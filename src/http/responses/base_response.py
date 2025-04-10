from typing import Any

from abc import ABC, abstractmethod

from aiohttp import ClientResponse


class BaseResponse(ABC):
    @staticmethod
    def is_ok(response: "ClientResponse") -> bool:
        return 200 <= response.status < 300

    @abstractmethod
    async def fetch(self, response: "ClientResponse") -> Any:
        raise NotImplemented
