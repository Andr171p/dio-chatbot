from abc import ABC, abstractmethod

from fastapi import UploadFile


class BaseUploadFileSaver(ABC):
    _upload_file: UploadFile

    @abstractmethod
    async def save(self) -> str:
        """Returning file path of saved file"""
        raise NotImplemented
