import logging

from src.presentation.api.app import get_fastapi_app


logging.basicConfig(level=logging.INFO)

app = get_fastapi_app()


'''import asyncio

from src.core.use_cases import ChatAssistant
from src.di.container import container


async def main() -> None:
    chat_assistant = await container.get(ChatAssistant)
    answer = await chat_assistant.answer("5", "Какая стоимость МЕТОДИЧЕСКИЕ И ДЕМОНСТРАЦИОННЫЕ МАТЕРИАЛЫ")
    print(answer)


asyncio.run(main())'''
