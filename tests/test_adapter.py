import asyncio

from crypto_mcp.adapters.mock_adapter import MockAdapter


async def _run_test():
    m = MockAdapter()
    t = await m.fetch_ticker("BTC/USDT")
    assert t["symbol"] == "BTC/USDT"
    o = await m.fetch_ohlcv("BTC/USDT", limit=5)
    assert len(o) == 5


def test_mock_adapter_loop():
    asyncio.get_event_loop().run_until_complete(_run_test())
