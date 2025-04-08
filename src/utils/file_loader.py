from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader
)


class FileLoader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @property
    def file_extension(self) -> str:
        return self.file_path.split(".")[-1]

    @property
    def file_name(self) -> str:
        return self.file_path.split("\\")[-1].split(".")[0]

    async def load(self) -> List[Document]:
        loader = TextLoader(self.file_path)
        if self.file_extension in ("xls", "xlsx"):
            loader = UnstructuredExcelLoader(self.file_path)
        elif self.file_extension in ("doc", "docx"):
            loader = Docx2txtLoader(self.file_path)
        documents = await loader.aload()
        return documents
