from crypto_mcp.utils.cache import TTLCache
import time


def test_cache_set_get():
    c = TTLCache(ttl_seconds=1)
    c.set("k", 123)
    assert c.get("k") == 123
    time.sleep(1.2)
    assert c.get("k") is None
