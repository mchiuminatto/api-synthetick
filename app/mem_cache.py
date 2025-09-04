import redis


class MemCache:
    def __init__(self, host="localhost", port=6379, db=0):
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
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)
