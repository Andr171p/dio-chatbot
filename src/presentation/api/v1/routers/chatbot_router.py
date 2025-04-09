from typing import List

from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.core.use_cases import ChatBotUseCase
from src.core.entities import ChattingUser


chatbot_router = APIRouter(
    prefix="/api/v1/chatbot",
    tags=["ChatBot"],
    route_class=DishkaRoute
)

active_connections: List[WebSocket] = []


@chatbot_router.websocket(path="/ws")
async def chat(
        websocket: WebSocket,
        chatting_user: ChattingUser,
        chatbot_use_case: FromDishka[ChatBotUseCase]
) -> ...:
    ...
