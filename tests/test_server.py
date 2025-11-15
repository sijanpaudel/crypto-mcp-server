import asyncio
from fastapi.testclient import TestClient

from crypto_mcp.server import app


def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_tick_cached():
    client = TestClient(app)
    r = client.get("/tick", params={"symbol": "BTC/USDT"})
    assert r.status_code == 200
    data = r.json()
    assert data.get("symbol") == "BTC/USDT"
