from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject

from src.core.use_cases import ChatAssistant
from src.presentation.api.v1.models import ChatResponse
from src.services.connection_managers import BaseConnectionManager


chat_socket_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Chat with AI assistant in real time"],
    route_class=DishkaRoute
)


@chat_socket_router.websocket("/{chat_id}")
@inject
async def chat(
        websocket: WebSocket,
        chat_id: str,
        chat_assistant: FromDishka[ChatAssistant],
        connection_manager: FromDishka[BaseConnectionManager]
):
    await connection_manager.connect(websocket, chat_id)
    try:
        while True:
            user_message = await websocket.receive_text()
            user_response = ChatResponse(role="User", message=user_message)
            await connection_manager.send(chat_id, user_response)
            assistant_message = await chat_assistant.answer(chat_id, user_message)
            assistant_response = ChatResponse(role="AI", message=assistant_message)
            await connection_manager.send(chat_id, assistant_response)
    except WebSocketDisconnect:
        await connection_manager.disconnect(chat_id)
