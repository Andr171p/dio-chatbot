from pydantic import BaseModel, Field


class Clarification(BaseModel):
    question: str = Field(description="")
