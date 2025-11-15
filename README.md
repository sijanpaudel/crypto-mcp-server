# Crypto MCP Server

A lightweight MCP-compatible server built with Python and FastAPI for fetching real-time and historical cryptocurrency market data using CCXT (with mock fallbacks).
Includes caching, error handling, tests, and clean abstractions for evaluation.

## 🚀 Features

- **HTTP Endpoints**
  - `/health` – Server status
  - `/tick?symbol=BTC/USDT` – Latest market price
  - `/historical?symbol=BTC/USDT&limit=50` – OHLCV historical data

- **WebSocket Endpoint**
  - `/ws` – Real-time price streaming (subscribe via JSON)

- **Adapters**
  - `CCXTAdapter` – Uses public exchange endpoints (no API key needed)
  - `MockAdapter` – Fallback when CCXT is unavailable

- **Other Features**
  - In-memory TTL caching
  - Simple error handling
  - Clean, modular architecture
  - Full test suite with pytest

## ⚙️ Installation & Setup

### 1. Create a virtual environment and install dependencies

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Optional (if using uv):
```
pip install uv
uv pip install -e .
```

### 2. Run the server locally

```
uvicorn crypto_mcp.server:app --reload
```

## 📡 API Examples

### Health Check
```
GET http://localhost:8000/health
```

### Latest Price
```
GET http://localhost:8000/tick?symbol=BTC/USDT
```

### Historical OHLCV Data
```
GET http://localhost:8000/historical?symbol=BTC/USDT&limit=50
```

## 🔗 Using Real Exchanges (CCXT)

Install CCXT:
```
pip install ccxt
```

### Public Market Data (No API key required)

You can fetch:
- Tickers
- OHLCV
- Orderbooks

using public, unauthenticated endpoints.

### Optional: API keys for private endpoints

```
export BINANCE_APIKEY="your_key"
export BINANCE_SECRET="your_secret"
```

Supported exchanges:
binance, kraken, coinbasepro, bybit, bitfinex

Test the CCXT adapter:
```
pytest tests/test_ccxt_adapter.py
```

## 🧪 Running Tests

```
pytest -q
```

## 📝 Assumptions & Notes

This is a minimal demo designed for the internship assignment.
In production systems, you would:

- Add proper adapter configuration and secrets management
- Use retry/backoff handling for exchange rate limits
- Use distributed caching (Redis) for data sharing
- Add integration tests with sandbox exchanges
- Implement structured logging and monitoring

## 📄 License

This project is released under the MIT License.
See the LICENSE file for details.