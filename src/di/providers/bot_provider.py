from dishka import Provider, provide, Scope

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.settings import settings


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return Bot(
            token=settings.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
