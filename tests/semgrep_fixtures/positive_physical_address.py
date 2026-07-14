def test_cache_identity(cache):
    assert id(cache.get("key")) == 140234567
