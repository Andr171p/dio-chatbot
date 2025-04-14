from datetime import datetime

from sqlalchemy import Text, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.types import RolesEnum
from src.database.models.base_model import BaseModel


class MessageModel(BaseModel):
    role: Mapped[RolesEnum] = mapped_column(default=RolesEnum.USER, server_default=text("'USER'"))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
