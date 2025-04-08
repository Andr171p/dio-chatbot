import logging
from pathlib import Path
from typing import Any, Union

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent.state import State
from src.ai_agent.nodes.base_node import BaseNode

from src.misc.file_readers import read_txt


log = logging.getLogger(__name__)


class GenerationNode(BaseNode):
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

    async def generate(self, query: str, context: str) -> str:
        chain = self._create_chain()
        generation = await chain.ainvoke({"query": query, "context": context})
        return generation

    async def ainvoke(self, state: State) -> dict[str, Any]:
        log.info("---GENERATE---")
        generation = await self.generate(state["summarized_message"], state["context"])
        return {"generation": generation}
