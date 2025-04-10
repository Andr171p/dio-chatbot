'''import logging

from src.presentation.api.app import get_fastapi_app


logging.basicConfig(level=logging.INFO)

app = get_fastapi_app()'''

import asyncio

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
    HumanMessage(content="Какая погода в Тюмени?")
]


async def main() -> None:
    res = await model_with_tools.ainvoke(messages)
    print(res)


# res = model_with_tools.invoke(messages)

asyncio.run(main())
