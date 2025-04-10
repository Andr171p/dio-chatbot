from typing import Optional

from aiohttp import ClientSession


class BaseHTTP:
    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    async def http_session(self) -> None:
        self._session = ClientSession()

    async def __aenter__(self) -> "BaseHTTP":
        await self.http_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.close()
        self._session = None
