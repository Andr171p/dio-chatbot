from typing import Literal, Union

from pydantic import BaseModel, field_validator


class UserMessage(BaseModel):
    chat_id: str
    content: str


class ChatBotMessage(BaseModel):
    content: str


class ChatResponse(BaseModel):
    role: Literal["user", "chatbot"] = "user"
    message: Union[UserMessage, ChatBotMessage]

    @field_validator("role")
    def set_role(cls, message: Union[UserMessage, ChatBotMessage]) -> Literal["user", "chatbot"]:
        role: Literal["user", "chatbot"] = "user"
        if isinstance(message, ChatBotMessage):
            role = "chatbot"
        return role
