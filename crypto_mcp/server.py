"""Simple MCP server based on FastAPI that follows a FastMCP-like interface.

Provides endpoints:
- GET /health
- GET /tick?symbol=BTC/USDT&exchange=binance  -> latest price
- GET /historical?symbol=BTC/USDT&exchange=binance&limit=100 -> OHLCV
- WebSocket /ws for real-time tick pushes (subscribe message required)

This is intentionally lightweight and designed for the assignment/demo.
"""
from typing import Optional, Dict, Any
import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

from .adapters import get_adapter
from .utils.cache import TTLCache
from .exceptions import AdapterError

logger = logging.getLogger("crypto_mcp")

app = FastAPI(title="crypto-mcp ")

# Simple in-memory cache for recent tick responses
cache = TTLCache(ttl_seconds=5)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tick")
async def tick(symbol: str, exchange: Optional[str] = "binance") -> Any:
    key = f"tick:{exchange}:{symbol}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    adapter = get_adapter(exchange)
    try:
        data = await adapter.fetch_ticker(symbol)
    except AdapterError as e:
        logger.exception("Adapter error")
        # Return 400 for unsupported symbol, 502 for other errors
        if "does not support symbol" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=502, detail=str(e))

    cache.set(key, data)
    return data


@app.get("/historical")
async def historical(symbol: str, exchange: Optional[str] = "binance", limit: int = 100) -> Any:
    adapter = get_adapter(exchange)
    try:
        data = await adapter.fetch_ohlcv(symbol, limit=limit)
    except AdapterError as e:
        logger.exception("Adapter error")
        if "does not support symbol" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=502, detail=str(e))
    return data


class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active.pop(client_id, None)

    async def send(self, client_id: str, message: dict):
        ws = self.active.get(client_id)
        if ws:
            await ws.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Simple protocol: client sends JSON {"op":"subscribe","symbol":"BTC/USDT","exchange":"binance","id":"client1"}
    try:
        init = await websocket.receive_json()
    except Exception:
        await websocket.close()
        return

    client_id = init.get("id", "anon")
    await manager.connect(websocket, client_id)

    try:
        if init.get("op") != "subscribe":
            await websocket.send_json({"error": "first message must be a subscribe op"})
            await websocket.close()
            return

        symbol = init.get("symbol")
        exchange = init.get("exchange", "binance")
        adapter = get_adapter(exchange)

        # simple loop: push a tick every 1s
        while True:
            try:
                tick = await adapter.fetch_ticker(symbol)
            except AdapterError as e:
                await websocket.send_json({"error": str(e)})
                break

            await websocket.send_json({"type": "tick", "symbol": symbol, "exchange": exchange, "data": tick})
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    finally:
        manager.disconnect(client_id)
