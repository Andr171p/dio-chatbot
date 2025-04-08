from dishka import make_async_container

from src.di.providers import LangchainProvider, ChatBotProvider


container = make_async_container(
    LangchainProvider(),
    ChatBotProvider()
)
