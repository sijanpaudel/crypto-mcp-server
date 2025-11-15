"""Adapter that uses ccxt if available. Falls back to raising AdapterError if ccxt missing.
"""
from typing import Any, List
from .mock_adapter import MockAdapter
from ..exceptions import AdapterError

try:
    import ccxt.async_support as ccxt
except Exception:
    ccxt = None



class CCXTAdapter:
    def __init__(self, exchange_name: str = "binance", api_key: str = None, secret: str = None):
        if ccxt is None:
            raise AdapterError("ccxt is not installed")
        self.exchange_name = exchange_name
        exchange_class = getattr(ccxt, exchange_name)
        if api_key and secret:
            self._exchange = exchange_class({"apiKey": api_key, "secret": secret})
        else:
            self._exchange = exchange_class()

    async def fetch_ticker(self, symbol: str) -> Any:
        if ccxt is None:
            return await MockAdapter().fetch_ticker(symbol)
        try:
            result = await self._exchange.fetch_ticker(symbol)
        except Exception as e:
            # Always close the exchange connection
            await self._exchange.close()
            # Handle unsupported symbol error
            if hasattr(e, 'args') and e.args and 'does not have market symbol' in str(e.args[0]):
                raise AdapterError(f"Exchange does not support symbol: {symbol}")
            raise AdapterError(f"Exchange error: {e}")
        await self._exchange.close()
        return result

    async def fetch_ohlcv(self, symbol: str, limit: int = 100, timeframe: str = "1m") -> List[List[float]]:
        if ccxt is None:
            return await MockAdapter().fetch_ohlcv(symbol, limit=limit)
        try:
            result = await self._exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            await self._exchange.close()
            if hasattr(e, 'args') and e.args and 'does not have market symbol' in str(e.args[0]):
                raise AdapterError(f"Exchange does not support symbol: {symbol}")
            raise AdapterError(f"Exchange error: {e}")
        await self._exchange.close()
        return result
