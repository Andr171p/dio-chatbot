from pydantic import BaseModel, Field


class ContextReply(BaseModel):
    context: str = Field(description="контекст извлечённый из базы знаний")
