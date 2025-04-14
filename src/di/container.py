from dishka import make_async_container

from src.di.providers import (
    LangchainProvider,
    ChatBotProvider,
    ServiceProvider,
    BotProvider
)


container = make_async_container(
    LangchainProvider(),
    ChatBotProvider(),
    ServiceProvider(),
    BotProvider()
)
