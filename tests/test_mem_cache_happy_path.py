from app.common.mem_cache import MemCacheFactory



class TestMemCache:
    def setup_method(self):
        self.mem_cache = MemCacheFactory.get_cache("redis")
        self.test_request_id = "TESTREQUEST12345"
        self.test_key = "test_key"
        self.test_value = "2000"


    def test_set_and_get(self):
        # Test setting a value
        self.mem_cache.set(self.test_request_id, self.test_key, self.test_value)


        # Test getting the value
        get_result = self.mem_cache.get(self.test_request_id, self.test_key)
        assert get_result == self.test_value

    def test_delete(self):
        # Set a value first
        self.mem_cache.set(self.test_request_id, self.test_key, self.test_value)

        # Now delete it
        delete_result = self.mem_cache.delete(self.test_request_id, self.test_key)
        assert delete_result == 1  # Redis returns the number of keys that were removed

        # Ensure it's deleted
        get_result = self.mem_cache.get(self.test_request_id, self.test_key)
        assert get_result is None