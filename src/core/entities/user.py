from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    username: str
    email: str


class AskingUser(BaseModel):
    chat_id: str
    user_message: str
