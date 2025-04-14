from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.chat_model import ChatModel

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import BaseModel


class UserModel(BaseModel):
    user_id: Mapped[str] = mapped_column(String(36))
    chats: Mapped[list["ChatModel"]] = ...
