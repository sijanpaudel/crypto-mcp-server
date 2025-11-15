import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from crypto_mcp.adapters.ccxt_adapter import CCXTAdapter
from crypto_mcp.exceptions import AdapterError

@pytest.mark.asyncio
async def test_ccxt_adapter_fetch_ticker_and_ohlcv():
    # Patch ccxt and its exchange class
    with patch("crypto_mcp.adapters.ccxt_adapter.ccxt") as ccxt_mod:
        class DummyExchange:
            async def fetch_ticker(self, symbol):
                return {"symbol": symbol, "last": 123.45}
            async def fetch_ohlcv(self, symbol, timeframe="1m", limit=100):
                return [[1,2,3,4,5,6]] * limit
            async def close(self):
                pass
        ccxt_mod.binance = lambda params=None: DummyExchange()
        adapter = CCXTAdapter("binance", api_key="k", secret="s")
        ticker = await adapter.fetch_ticker("BTC/USDT")
        assert ticker["symbol"] == "BTC/USDT"
        ohlcv = await adapter.fetch_ohlcv("BTC/USDT", limit=2)
        assert len(ohlcv) == 2


def test_ccxt_adapter_no_ccxt():
    # Patch ccxt to None
    with patch("crypto_mcp.adapters.ccxt_adapter.ccxt", None):
        with pytest.raises(AdapterError):
            CCXTAdapter("binance")
