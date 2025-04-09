from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    username: str


class ChattingUser(BaseModel):
    chat_id: str
    username: str
