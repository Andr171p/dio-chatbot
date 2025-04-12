from langchain_core.language_models import BaseChatModel

from src.yandex_gpt.api import YandexGPTAPI
from src.yandex_gpt.base import _BaseYandexGPT


class YandexGPTChatModel(_BaseYandexGPT, BaseChatModel):
    ...