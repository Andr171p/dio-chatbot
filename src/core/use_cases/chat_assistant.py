from src.ai_agent import BaseAgent
from src.core.entities import AskingUser


class ChatAssistant:
    def __init__(self, ai_agent: BaseAgent) -> None:
        self._ai_agent = ai_agent

    async def answer(self, asking_user: AskingUser) -> str:
        return await self._ai_agent.generate(**asking_user.model_dump())

    async def chat(self, chat_id: str, user_message: str) -> str:
        ...
