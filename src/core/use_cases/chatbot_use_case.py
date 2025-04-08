from src.ai_agent import BaseAgent


class ChatBotUseCase:
    def __init__(self, ai_agent: BaseAgent) -> None:
        self._ai_agent = ai_agent

    async def answer(self, user_id: str, user_message: str) -> str:
        return await self._ai_agent.generate(user_id, user_message)

    async def chat(self, user_id: str, user_message: str) -> str:
        ...
