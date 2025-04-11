from typing import Literal


URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

AVAILABLE_MODELS = Literal[
    "yandexgpt",
    "yandexgpt-lite"
]
