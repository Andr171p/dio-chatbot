import logging
from pathlib import Path
from typing import Literal, Union

from langgraph.types import Command

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel, LLM
from langchain_core.output_parsers import PydanticOutputParser

from src.ai_agent.states import State
from src.ai_agent.schemas import Decision
from src.ai_agent.utils import format_messages
from src.ai_agent.nodes.base_node import BaseNode

from src.services import ChatHistory
from src.misc.file_readers import read_txt


log = logging.getLogger(__name__)


AllowedCommands = Literal["retrieval", "clarification"]


class DecisionNode(BaseNode):
    def __init__(
            self,
            chat_history: ChatHistory,
            template_path: Union[Path, str],
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._chat_history = chat_history
        self._template_path = template_path
        self._model = model

    def _create_chain(self) -> Runnable:
        parser = PydanticOutputParser(pydantic_object=Decision)
        prompt = (
            ChatPromptTemplate
            .from_messages([("system.txt", read_txt(self._template_path))])
            .partial(format_instructions=parser.get_format_instructions())
        )
        return prompt | self._model | parser

    async def _get_dialog(self, user_id: str, user_message: str) -> str:
        messages = await self._chat_history.get_messages(user_id)
        dialog = format_messages(user_message, messages)
        return dialog

    async def decide(self, user_id: str, user_message: str) -> dict[str, str]:
        chain = self._create_chain()
        dialog = await self._get_dialog(user_id, user_message)
        decision = await chain.ainvoke({"dialog": dialog})
        next_step = decision.next_step
        return next_step

    async def ainvoke(self, state: State) -> Command[AllowedCommands]:
        log.info("---DECISION---")
        dialog = await self._get_dialog(state["user_id"], state["user_message"])
        next_step = await self.decide(state["user_id"], state["user_message"])
        return Command(
            update={"dialog": dialog},
            goto=next_step
        )
