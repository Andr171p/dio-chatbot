from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.retrievers import BaseRetriever

from src.ai_agent.utils import format_documents

from src.misc.file_readers import read_txt
from src.settings import settings


class RetrievalTool(BaseTool):
    name = "RetrievalTool"
    description = read_txt(settings.prompt.retrival_description_path)

    def __init__(self, retriever: BaseRetriever, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._retriever = retriever

    def _run(self, query: str) -> str:
        documents = self._retriever.invoke(query)
        context = format_documents(documents)
        return context

    async def _arun(self, query: str) -> str:
        documents = await self._retriever.ainvoke(query)
        context = format_documents(documents)
        return context
