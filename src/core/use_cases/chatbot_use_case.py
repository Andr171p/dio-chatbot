from src.ai_agent import BaseAgent


class ChatBotUseCase:
    def __init__(self, ai_agent: BaseAgent) -> None:
        self._ai_agent = ai_agent

    async def answer(self, ) -> str:
        ...

    async def chat(self, ) -> str:
        ...
