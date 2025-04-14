__all__ = (
    "chat_router",
    "documents_router",
    "socket_chat_router"
)

from src.presentation.api.v1.routers.chat import chat_router
from src.presentation.api.v1.routers.documents import documents_router
from src.presentation.api.v1.routers.socket_chat import socket_chat_router
