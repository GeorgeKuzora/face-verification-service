import logging
import pickle  # noqa: S403 considered
from typing import Any

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from app.core import models as srv
from app.core.config import get_settings
from app.external.postgres import models as db

logger = logging.getLogger(__name__)


def create_pool() -> Engine:
    """
    Создает sqlalchemy engine с пулом соединений.

    :return: sqlalchemy engine с пулом соединений.
    :rtype: Engine
    """
    settings = get_settings()
    return create_engine(
        str(settings.postgres.pg_dns),
        pool_size=settings.postgres.pool_size,
        max_overflow=settings.postgres.max_overflow,
    )


def create_all_tables() -> None:
    """Создает таблицы в базе данных."""
    pool = create_pool()
    db.Base.metadata.create_all(pool)


class DBStorage:
    """База данных."""

    def __init__(self) -> None:
        """Метод инициализации."""
        self.pool = create_pool()

    def update_user(
        self, vector: list[dict[str, Any]], username: str,
    ) -> srv.User | None:
        """
        Метод обновления пользователя.

        Устанавливает поле is_verified на true.

        :param username: Имя пользователя
        :type username: str
        :param vector: Вектор лица пользователя
        :type vector: list[dict[str, Any]]
        :return: Обновленный пользователь.
        :rtype: srv.User | None
        """
        with Session(self.pool) as session:
            user = self._get_user(username, session)
            if not user or user.is_deleted is True:
                logger.error(f'{username} not found')
                return None
            user.is_verified = True
            user.vector = self._pickle_vector(vector)
            logger.info(f'{username}.is_verified set to True')
            srv_user = self._get_srv_user(user, vector)
            session.commit()
        return srv_user

    def _get_user(self, username, session: Session) -> db.User | None:
        return session.scalars(
            select(db.User).where(db.User.username == username),
        ).first()

    def _get_srv_user(
        self, db_user: db.User, vector: list[dict[str, Any]] | None = None,  # noqa: WPS221, E501
    ) -> srv.User:
        return srv.User(
            username=db_user.username,
            is_verified=db_user.is_verified,
            user_id=db_user.id,
            vector=vector,
        )

    def _pickle_vector(self, vector: list[dict[str, Any]]) -> bytes:
        return pickle.dumps(vector)
