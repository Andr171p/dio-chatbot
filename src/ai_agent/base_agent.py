from typing import Any
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseAgent(ABC):
    @abstractmethod
    async def generate(self, thread_id: str, query: str) -> str:
        raise NotImplemented

    @abstractmethod
    async def stream(self, thread_id: int, query: str) -> AsyncGenerator[str, Any]:
        raise NotImplemented
