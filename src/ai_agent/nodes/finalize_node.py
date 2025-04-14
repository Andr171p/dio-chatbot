import logging

from typing import Any, Optional

from src.ai_agent.states import State
from src.ai_agent.nodes.base_node import BaseNode

from src.services import ChatHistory
from src.handlers import message_saver


log = logging.getLogger(__name__)


class FinalizeNode(BaseNode):
    def __init__(self, chat_history: ChatHistory) -> None:
        self._chat_history = chat_history

    @staticmethod
    def finalize(generation: Optional[str], clarifying_question: Optional[str]) -> str:
        final_answer = generation
        if generation is None and clarifying_question:
            final_answer = clarifying_question
        return final_answer

    async def ainvoke(self, state: State) -> dict[str, Any]:
        log.info("---FINALIZE---")
        generation: Optional[str] = state.get("generation")
        clarifying_question: Optional[str] = state.get("clarifying_question")
        final_answer = self.finalize(generation, clarifying_question)
        return {"final_answer": final_answer}
