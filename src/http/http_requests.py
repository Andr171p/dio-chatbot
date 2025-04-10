from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aiohttp import ClientSession, ClientResponse

from src.http.responses.base_response import BaseResponse


class HTTPRequests:
    _session: "ClientSession"

    def __init__(self, response_type: BaseResponse) -> None:
        self._response_type = response_type

    @staticmethod
    def is_ok(response: "ClientResponse") -> bool:
        return 200 <= response.status < 300

    async def get(
            self,
            url: str,
            headers: Optional[dict] = None,
            timeout: int = 10
    ) -> Any:
        async with self._session.get(
            url=url,
            headers=headers,
            timeout=timeout
        ) as response:
            return await self._response_type.fetch(response)

    async def post(
            self,
            url: str,
            json: dict,
            headers: Optional[dict] = None,
            timeout: int = 10
    ) -> Any:
        async with self._session.post(
            url=url,
            json=json,
            headers=headers,
            timeout=timeout
        ) as response:
            return await self._response_type.fetch(response)
