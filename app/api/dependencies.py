import redis

from app.constants import REDIS_DB, REDIS_HOST, REDIS_PORT


def create_redis():
    return redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True, encoding="UTF-8"
                                )


pool = create_redis()
