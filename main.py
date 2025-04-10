'''import logging

from src.presentation.api.app import get_fastapi_app


logging.basicConfig(level=logging.INFO)

app = get_fastapi_app()'''

from src.settings import settings
from src.llms.yandex_gpt import YandexGPTChatModel

from langchain_core.tools import BaseTool, tool
from langchain_core.messages import HumanMessage


@tool
def get_weather(city: str) -> str:
    """Получить текущую погоду в указанном городе."""
    return f"Погода в {city}: 25°C, солнечно"


model = YandexGPTChatModel(
    folder_id=settings.yandex_gpt.folder_id,
    api_key=settings.yandex_gpt.api_key,
    model_name="yandexgpt"
)

model_with_tools = model.bind_tools([get_weather])

messages = [
    HumanMessage(content="Какая погода в Москве?")
]


res = model_with_tools.invoke(messages)

print(res)
