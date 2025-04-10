from typing import Optional

from aiohttp import ClientResponse

from src.http.responses.base_response import BaseResponse


class JsonResponse(BaseResponse):
    async def fetch(self, response: "ClientResponse") -> Optional[dict]:
        if not self.is_ok(response):
            return None
        return await response.json()
