from typing import Literal

from pydantic import BaseModel


class ChatResponse(BaseModel):
    role: Literal["user", "assistant"] = "user"
    message: str

