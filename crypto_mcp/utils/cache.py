"""Simple TTL in-memory cache used for demo/testing."""
import time
from typing import Any, Optional


class TTLCache:
    def __init__(self, ttl_seconds: int = 5):
        self.ttl = ttl_seconds
        self._store = {}

    def get(self, key: str) -> Optional[Any]:
        rec = self._store.get(key)
        if not rec:
            return None
        value, expires = rec
        if time.time() > expires:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, time.time() + self.ttl)

    def clear(self):
        self._store.clear()
