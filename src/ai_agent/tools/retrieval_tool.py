import logging

from typing import Any, Type, Optional, List

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.misc.files import read_txt
from src.settings import settings


log = logging.getLogger(__name__)


def format_documents(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


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
        return format_documents(documents)

    async def _arun(self, query: str) -> str:
        log.info("---RETRIEVE---")
        documents = await self._retriever.ainvoke(query)
        return format_documents(documents)
