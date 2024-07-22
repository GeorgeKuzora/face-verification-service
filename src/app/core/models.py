from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    """Соощение от очереди сообщений."""

    path: Path | str
    username: str


class User(BaseModel):
    """Пользователь."""

    username: str
    representation: list[dict[str, Any]]
    user_id: int | None = None
