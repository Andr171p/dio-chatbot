import aioredis

from typing import Optional


class RedisConnection:
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None
    ) -> None:
        self.__host = host
        self.__port = port
        self.__db = db
        self.__password = password
        self._redis: Optional[aioredis.Redis] = None

    @property
    def url(self) -> str:
        return f"redis://{self.__host}:{self.__port}/{self.__db}"

    async def _connect(self) -> None:
        self._redis = await aioredis.from_url(
            url=self.url,
            password=self.__password,
            decode_response=True
        )

    async def _close(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def __aenter__(self) -> "RedisConnection":
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._close()
