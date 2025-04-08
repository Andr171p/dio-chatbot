from typing import Literal

from pydantic import BaseModel


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    thread_id: str
    content: str


class ChatBotMessage(BaseModel):
    role: Literal["chatbot"] = "chatbot"
    content: str

    @classmethod
    def from_string(cls, string: str) -> "ChatBotMessage":
        return cls(content=string)
