from typing import TYPE_CHECKING, Any, Optional, List

if TYPE_CHECKING:
    from aioredis import Redis


TTL = 1800


class RedisCRUD:
    _redis: "Redis"

    async def create(self, key: str, value: Any, ttl: Optional[int] = TTL) -> bool:
        return await self._redis.set(key, value, ex=ttl)

    async def read(self, key: str) -> Optional[Any]:
        return await self._redis.get(key)

    async def update(self, key: str, value: Any, ttl: Optional[int] = TTL) -> bool:
        return await self.create(key, value, ttl)

    async def delete(self, key: str) -> bool:
        return await self._redis.delete(key) > 0

    async def push_list(self, key: str, value: Any, left: bool = True) -> int:
        if left:
            return await self._redis.lpush(key, value)
        return await self._redis.rpush(key, value)

    async def read_list(self, key: str, start: int = 0, end: int = -1) -> List[Optional[Any]]:
        return await self._redis.lrange(key, start, end)
