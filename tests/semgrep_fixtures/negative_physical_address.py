def test_cache_value(cache, expected_value):
    assert cache.get("key") == expected_value
