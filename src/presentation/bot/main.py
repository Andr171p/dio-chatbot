from aiogram import Bot

from src.di.container import container
from src.presentation.bot.app import create_aiogram_app


async def run_bot() -> None:
    bot = await container.get(Bot)
    app = create_aiogram_app()
    await bot.delete_webhook(drop_pending_updates=True)
    await app.start_polling(bot, allowed_updates=app.resolve_used_update_types())
