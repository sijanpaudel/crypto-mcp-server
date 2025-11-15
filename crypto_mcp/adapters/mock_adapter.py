"""A mock adapter used for testing and when CCXT is not available.

It implements async-friendly methods: fetch_ticker and fetch_ohlcv.
"""
from typing import Any, List
import time

class MockAdapter:
    async def fetch_ticker(self, symbol: str) -> Any:
        # return a synthetic ticker
        now = int(time.time() * 1000)
        return {
            "symbol": symbol,
            "timestamp": now,
            "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now/1000)),
            "high": 1.0,
            "low": 0.9,
            "bid": 0.95,
            "ask": 0.96,
            "last": 0.955,
            "baseVolume": 12345,
        }

    async def fetch_ohlcv(self, symbol: str, limit: int = 100) -> List[List[float]]:
        # generate fake OHLCV: [timestamp, open, high, low, close, volume]
        now = int(time.time())
        data = []
        for i in range(limit):
            ts = (now - i * 60) * 1000
            o = 1.0
            h = 1.01
            l = 0.99
            c = 1.0
            v = 100
            data.append([ts, o, h, l, c, v])
        return list(reversed(data))
