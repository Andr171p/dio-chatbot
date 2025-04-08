from pydantic import BaseModel, Field


class Decision(BaseModel):
    next_step: str = Field(description="Твой ответ должен содержать только retrieval или clarification")
