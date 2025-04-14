from aiogram import F, Router
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

from src.core.use_cases import ChatAssistant


chat_router = Router()


@chat_router.message(F.text)
async def chat(message: Message, chat_assistant: FromDishka[ChatAssistant]) -> None:
    user_id: int = message.from_user.id
    text: str = message.text
    assistant_message = await chat_assistant.answer(str(user_id), text)
    await message.answer(assistant_message)
