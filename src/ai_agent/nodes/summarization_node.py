import logging
from pathlib import Path
from typing import Any, Union

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent.states import State
from src.ai_agent.nodes.base_node import BaseNode

from src.misc.file_readers import read_txt


log = logging.getLogger(__name__)


class SummarizationNode(BaseNode):
    def __init__(
            self,
            template_path: Union[Path, str],
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._template_path = template_path
        self._model = model

    def _create_chain(self) -> Runnable:
        prompt = ChatPromptTemplate.from_template(read_txt(self._template_path))
        return prompt | self._model | StrOutputParser()

    async def summarize(self, dialog: str) -> str:
        chain = self._create_chain()
        summarized_message = await chain.ainvoke({"dialog": dialog})
        return summarized_message

    async def ainvoke(self, state: State) -> dict[str, Any]:
        log.info("---SUMMARIZATION---")
        summarized_message = await self.summarize(state["dialog"])
        return {"summarized_message": summarized_message}
