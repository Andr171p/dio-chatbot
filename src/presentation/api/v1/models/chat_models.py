from typing import Literal

from pydantic import BaseModel


class ChatResponse(BaseModel):
    role: Literal["User", "AI"]
    message: str
