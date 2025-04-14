import logging

from typing import Any, Type, Optional

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.retrievers import BaseRetriever

from src.ai_agent.utils import format_documents

from src.misc.files import read_txt
from src.settings import settings


log = logging.getLogger(__name__)


class RetrievalToolInput(BaseModel):
    query: str = Field(..., description="Запрос для поиска релевантных документов с продуктами 1С")


class RetrievalTool(BaseTool):
    name: str = "RetrievalTool"
    description: str = read_txt(settings.prompts.retrival_description_path)
    args_schema: Optional[Type[BaseModel]] = RetrievalToolInput

    def __init__(self, retriever: BaseRetriever, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._retriever = retriever

    def _run(self, query: str) -> str:
        log.info("---RETRIEVE---")
        documents = self._retriever.invoke(query)
        context = format_documents(documents)
        return context

    async def _arun(self, query: str) -> str:
        log.info("---RETRIEVE---")
        documents = await self._retriever.ainvoke(query)
        context = format_documents(documents)
        return context
