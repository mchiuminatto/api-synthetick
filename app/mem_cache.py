import redis
import app.constants as const


class MemCache:
    def __init__(self, **kwargs):
        pass

    def set(self, key, value):
        pass

    def get(self, key):
        pass


class MemCacheFactory:
    @staticmethod
    def create_mem_cache(technology: str) -> MemCache:

        if technology == "redis":
            return RedisMemCache()


class RedisMemCache(MemCache):
    def __init__(self):
        self.client = redis.Redis(host=const.REDIS_HOST, 
                                  port=const.REDIS_PORT, 
                                  db=const.REDIS_DB)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)
