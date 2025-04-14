from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    Docx2txtLoader,
    UnstructuredPDFLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader
)


SUPPORTED_EXTENSIONS = {
    "txt": TextLoader,
    "pdf": UnstructuredPDFLoader,
    "docx": Docx2txtLoader,
    "doc": Docx2txtLoader,
    "xls": UnstructuredExcelLoader,
    "xlsx": UnstructuredExcelLoader,
    "pptx": UnstructuredPowerPointLoader,
    "ppt": UnstructuredPowerPointLoader,
}


class FileToDocumentsLoader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @property
    def file_extension(self) -> str:
        return self.file_path.split(".")[-1]

    @property
    def file_name(self) -> str:
        return self.file_path.split("\\")[-1].split(".")[0]

    async def load(self) -> Optional[List[Document]]:
        if self.file_extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file with extension {self.file_extension}")
        loader = SUPPORTED_EXTENSIONS[self.file_extension]
        documents = await loader(self.file_path).aload()
        return documents
