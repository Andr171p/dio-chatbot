import logging
from functools import wraps
from typing import (
    Callable,
    Coroutine,
    Any,
    TypeVar
)

from src.ai_agent.state import State


T = TypeVar("T", bound="FinalizeNode")

log = logging.getLogger(__name__)


def message_saver(
        func: Callable[[T, State, Any], Coroutine[Any, Any, dict[str, Any]]]
) -> Callable[[T, State, Any], Coroutine[Any, Any, dict[str, Any]]]:
    @wraps(func)
    async def wrapper(self: T, state: State, *args, **kwargs) -> dict[str, Any]:
        user_id: str = state.get("user_id")
        user_message: str = state.get("user_message")
        if user_id is None:
            raise ValueError("user_id is required")
        response = await func(self, state, *args, **kwargs)
        final_answer: str = response.get("final_answer")
        if self._chat_history:
            await self._chat_history.save_message(user_id, {"human": user_message})
            await self._chat_history.save_message(user_id, {"ai": final_answer})
            log.info("Messages saved successfully")
        return response
    return wrapper
