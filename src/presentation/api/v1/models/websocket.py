from pydantic import BaseModel


class OnAccept(BaseModel):
    detail: str = "connected"


class OnDisconnect(BaseModel):
    detail: str = "disconnected"
