from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    """Сообщение от очереди сообщений."""

    path: Path | str
    username: str


class User(BaseModel):
    """Пользователь."""

    username: str
    is_verified: bool
    vector: list[dict[str, Any]] | None = None
    user_id: int | None = None
