from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dishka.integrations.aiogram import setup_dishka

from src.presentation.bot.routers import chat_router
from src.di.container import container


def create_aiogram_app() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(chat_router)
    setup_dishka(
        container=container,
        router=dp,
        auto_inject=True
    )
    return dp
