from src.redis.redis_connection import RedisConnection
from src.redis.redis_crud import RedisCRUD


class RedisClient(RedisCRUD, RedisConnection):
    pass
