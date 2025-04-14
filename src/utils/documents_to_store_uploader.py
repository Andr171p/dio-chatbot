from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import ElasticSearchBM25Retriever


class DocumentsToStoreUploader:
    def __init__(
            self,
            vector_store: VectorStore,
            bm25_store: ElasticSearchBM25Retriever
    ) -> None:
        self._vector_store = vector_store
        self._bm25_store = bm25_store

    @property
    def _text_splitter(self) -> RecursiveCharacterTextSplitter:
        return RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=20,
            length_function=len
        )

    def _create_chunks(self, documents: List[Document]) -> List[Document]:
        return self._text_splitter.create_documents([document.page_content for document in documents])

    async def upload(self, documents: List[Document]) -> None:
        chunks = self._create_chunks(documents)
        self._vector_store.add_documents(chunks)
        self._bm25_store.add_texts([chunk.page_content for chunk in chunks])
