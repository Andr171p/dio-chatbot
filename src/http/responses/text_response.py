from typing import Optional

from aiohttp import ClientResponse

from src.http.responses.base_response import BaseResponse


class TextResponse(BaseResponse):
    async def fetch(self, response: "ClientResponse") -> Optional[str]:
        if not self.is_ok(response):
            return None
        return await response.text()
