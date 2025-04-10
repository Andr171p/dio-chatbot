from typing import Any, Union

from abc import ABC, abstractmethod

from langgraph.types import Command

from src.ai_agent.states import State


class BaseNode(ABC):
    @abstractmethod
    async def ainvoke(self, state: State) -> Union[dict[str, Any], Command]:
        raise NotImplemented

    async def __call__(self, state: State) -> Union[dict[str, Any], Command]:
        return await self.ainvoke(state)
