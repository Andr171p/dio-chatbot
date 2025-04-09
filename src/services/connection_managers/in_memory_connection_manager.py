import logging

from typing import Optional

from fastapi import WebSocket

from src.services.connection_managers.base_connection_manager import BaseConnectionManager


log = logging.getLogger(__name__)


class InMemoryConnectionManager(BaseConnectionManager):
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        log.debug("Created new active connection for %s", connection_id)

    async def disconnect(self, connection_id: str) -> None:
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            log.debug("Deleted connection for %s", connection_id)

    async def get_connection(self, connection_id: str) -> Optional[WebSocket]:
        return self.active_connections.get(connection_id)
