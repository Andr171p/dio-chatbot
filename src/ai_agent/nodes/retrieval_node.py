import logging

from typing import Any

from langchain_core.retrievers import BaseRetriever

from src.ai_agent.states import State
from src.ai_agent.utils import format_documents
from src.ai_agent.nodes.base_node import BaseNode


log = logging.getLogger(__name__)


class RetrievalNode(BaseNode):
    def __init__(self, retriever: BaseRetriever) -> None:
        self._retriever = retriever

    async def retrieve(self, query: str) -> str:
        documents = await self._retriever.ainvoke(query)
        context = format_documents(documents)
        return context

    async def ainvoke(self, state: State) -> dict[str, Any]:
        log.info("---RETRIEVE---")
        context = await self.retrieve(state["summarized_message"])
        return {"context": context}
