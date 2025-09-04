from app.mem_cache import MemCacheFactory


class TestMemCacheHappyPath:
    def test_mem_cache_happy_path(self):
        mem_cache = MemCacheFactory.create_mem_cache(technology="redis")
        
        test_key_1 = "hfkjshkjfs:status"
        test_key_2 = "hfkjshkjfs:records-generated"
        value_1 = "running"
        value_2 = 1000
        
        mem_cache.set(test_key_1, value_1)
        mem_cache.set(test_key_2, value_2)

        assert str(mem_cache.get(test_key_1), encoding="UTF-8") == value_1
        assert int(str(mem_cache.get(test_key_2), encoding="UTF-8")) == value_2
        