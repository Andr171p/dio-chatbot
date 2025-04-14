from abc import ABC, abstractmethod


class BaseUploadFileSaver(ABC):
    @abstractmethod
    async def save(self) -> str:
        """Returning file path of saved file"""
        raise NotImplemented
