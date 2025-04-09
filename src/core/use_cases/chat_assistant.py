from src.ai_agent import BaseAgent


class ChatAssistant:
    def __init__(self, ai_agent: BaseAgent) -> None:
        self._ai_agent = ai_agent

    async def answer(self, chat_id: str, user_message: str) -> str:
        return await self._ai_agent.generate(chat_id, user_message)

    async def chat(self, chat_id: str, user_message: str) -> str:
        ...
