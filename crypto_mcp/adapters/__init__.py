import os
from .ccxt_adapter import CCXTAdapter
from .mock_adapter import MockAdapter

def get_adapter(name: str):
    """
    Returns a CCXTAdapter for supported exchanges if ccxt is installed (uses public data if no API keys), else MockAdapter.
    """
    name = (name or "binance").lower()
    supported = {"binance", "kraken", "coinbasepro", "bybit", "bitfinex"}
    if name in supported:
        try:
            api_key = os.environ.get(f"{name.upper()}_APIKEY")
            secret = os.environ.get(f"{name.upper()}_SECRET")
            # If no keys, CCXTAdapter will use public mode
            return CCXTAdapter(exchange_name=name, api_key=api_key, secret=secret)
        except Exception:
            pass
    return MockAdapter()
