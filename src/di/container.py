from dishka import make_async_container

from src.di.providers import LangchainProvider


container = make_async_container(LangchainProvider())
