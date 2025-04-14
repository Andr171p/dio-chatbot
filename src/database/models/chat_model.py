from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.message_model import MessageModel

from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import BaseModel


class ChatModel(BaseModel):
    chat_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    messages: Mapped[list["MessageModel"]] = ...
