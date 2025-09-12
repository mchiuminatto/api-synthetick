import abc
import redis
from app.common.constants import REDIS_DB, REDIS_HOST, REDIS_PORT


class MemCache(abc.ABC):

    @abc.abstractmethod
    def get(self, request_id: str, value_key: str):
        pass

    def set(self, request_id: str, value_key: str, value):
        pass

    def delete(self, request_id: str, value_key: str):
        pass

class MemCacheFactory:
    @staticmethod
    def get_cache(cache_type: str) -> MemCache:
        if cache_type == "redis":
            return RedisCache()
        else:
            raise ValueError(f"Unsupported cache type: {cache_type}")


class RedisCache(MemCache):
    def __init__(self):
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True,
                                           encoding="UTF-8"
                                           )
        self._client = redis.Redis(connection_pool=pool)

    def get(self, request_id: str, value_key: str):
        return self._client.get(f"{request_id}:{value_key}")

    def set(self, request_id: str, value_key: str, value):
        self._client.set(f"{request_id}:{value_key}", value)

    def delete(self, request_id: str, value_key: str):
        return self._client.delete(f"{request_id}:{value_key}")

    def __del__(self):
        self._client.close()


mem_cache = MemCacheFactory.get_cache("redis")