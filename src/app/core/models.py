from pathlib import Path

from pydantic import BaseModel


class Message(BaseModel):
    """Соощение от очереди сообщений."""

    path: Path | str
    username: str


class User(BaseModel):
    """Пользователь."""

    username: str
    is_verified: bool
    user_id: int | None = None
