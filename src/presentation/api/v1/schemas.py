from typing import Literal

from pydantic import BaseModel


class ChatResponse(BaseModel):
    role: Literal["user", "assistant"] = "user"
    message: str

    @classmethod
    def from_user_message(cls, user_message: str) -> "ChatResponse":
        return cls(role="user", message=user_message)

    @classmethod
    def from_assistant_message(cls, assistant_message: str) -> "ChatResponse":
        return cls(role="assistant", message=assistant_message)

