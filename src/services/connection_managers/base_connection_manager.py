from typing import Optional

from abc import ABC, abstractmethod

from fastapi import WebSocket
from pydantic import BaseModel


class BaseConnectionManager(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        raise NotImplemented

    @abstractmethod
    async def disconnect(self, connection_id: str) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_connection(self, connection_id: str) -> Optional[WebSocket]:
        raise NotImplemented

    async def send(self, connection_id: str, json_model: BaseModel) -> None:
        connection = await self.get_connection(connection_id)
        if connection is None:
            return
        await connection.send_json(json_model.model_dump())
