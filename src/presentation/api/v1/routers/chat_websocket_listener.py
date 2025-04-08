from litestar import WebSocket
from litestar.handlers import WebsocketListener
from dishka.integrations.base import FromDishka
from dishka.integrations.litestar import inject

from src.core.use_cases import ChatBotUseCase
from src.presentation.api.v1.models import (
    OnAccept,
    OnDisconnect,
    UserMessage,
    ChatBotMessage
)


class ChatWebsocketListener(WebsocketListener):
    path = "/api/v1/chat"

    async def on_accept(self, socket: WebSocket) -> None:
        await socket.send_json(OnAccept().model_dump())

    async def on_disconnect(self, socket: WebSocket) -> None:
        await socket.send_json(OnDisconnect().model_dump())

    @inject
    async def on_receive(
            self,
            data: UserMessage,
            chatbot_use_case: FromDishka[ChatBotUseCase]
    ) -> ChatBotMessage:
        chatbot_answer = await chatbot_use_case.answer(data.thread_id, data.content)
        return ChatBotMessage.from_string(chatbot_answer)
