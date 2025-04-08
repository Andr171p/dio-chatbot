from typing import Any
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseAgent(ABC):
    @abstractmethod
    async def generate(self, *args) -> str:
        raise NotImplemented

    @abstractmethod
    async def stream(self, *args) -> AsyncGenerator[str, Any]:
        raise NotImplemented
