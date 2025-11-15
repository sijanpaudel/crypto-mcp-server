# crypto-mcp
License
--
This project is released under the MIT license. See `LICENSE`.

Overview
- HTTP endpoints: `/health`, `/tick`, `/historical`
- WebSocket endpoint: `/ws` (subscribe with JSON payload)
- Adapters: `MockAdapter` and `CCXTAdapter` (falls back to mock when ccxt not present)
- In-memory TTL cache and basic error handling

Quick start
1. Create a virtual environment and install dependencies listed in `pyproject.toml`.

   python -m venv .venv
   source .venv/bin/activate
   # Install `uv` first if you plan to use `uv` commands (optional). If you don't have
   # `uv` installed, you can install it via pip:
   python -m pip install --upgrade pip
   python -m pip install uv

   # Then you can use uv-based commands (example below uses `uv sync`).
   uv pip install -e .

   # Or just use
   pip install -e .

2. Run server locally:

   uvicorn crypto_mcp.server:app --reload


3. Examples
 - Health: GET http://localhost:8000/health
 - Tick: GET http://localhost:8000/tick?symbol=BTC/USDT
 - Historical: GET http://localhost:8000/historical?symbol=BTC/USDT&limit=50


Using real exchanges (CCXT)
--------------------------
To fetch real data from supported exchanges (e.g., binance, kraken, coinbasepro), install `ccxt`.

**No API keys are required for public market data.**
If you do not set API keys, the server will use public endpoints for price and OHLCV data

If you want to access private endpoints, set API keys as environment variables:

   export BINANCE_APIKEY=your_api_key
   export BINANCE_SECRET=your_secret

The server will use `CCXTAdapter` for these exchanges if `ccxt` is installed. If not, it falls back to the mock adapter.

Supported exchanges: binance, kraken, coinbasepro, bybit, bitfinex

You can test the CCXT adapter logic with:

   pytest tests/test_ccxt_adapter.py

Tests
Run tests with pytest:

   pytest -q

Assumptions and notes
- This is a minimal demo to showcase architecture, error handling, caching and tests. In production you would:
  - Introduce proper adapter configuration and credentials management
  - Use a resilient connection manager for exchanges (rate limits, retries)
  - Use persistent caching (Redis) for distributed deployments
  - Add more extensive test coverage (integration tests with a sandboxed exchange)


