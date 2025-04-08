import logging
from pathlib import Path
from typing import Any, Union

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel, LLM
from langchain_core.output_parsers import PydanticOutputParser

from src.ai_agent.state import State
from src.ai_agent.schemas import Clarification
from src.ai_agent.nodes.base_node import BaseNode

from src.misc.file_readers import read_txt


log = logging.getLogger(__name__)


class ClarificationNode(BaseNode):
    def __init__(
            self,
            template_path: Union[Path, str],
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._template_path = template_path
        self._model = model

    def _create_chain(self) -> Runnable:
        parser = PydanticOutputParser(pydantic_object=Clarification)
        prompt = (
            ChatPromptTemplate
            .from_messages([("system", read_txt(self._template_path))])
            .partial(format_instructions=parser.get_format_instructions())
        )
        return prompt | self._model | parser

    async def clarify(self, user_message: str) -> str:
        chain = self._create_chain()
        clarification = await chain.ainvoke({"user_message": user_message})
        return clarification.question

    async def ainvoke(self, state: State) -> dict[str, Any]:
        log.info("---CLARIFY---")
        clarifying_question = await self.clarify(state["user_message"])
        return {"clarifying_question": clarifying_question}
