import logging
from typing import Any

from app.core.models import User

logger = logging.getLogger(__name__)


class InMemoryStorage:
    """
    Имплементация хранилища данных в оперативной памяти.

    Сохраняет данные только на время работы программы.
    Для хранения данных использует списки python.

    Attributes:
        users: list[User] - созданные пользователи.
        users_count: int - счетчик созданных пользователей.
        tokens: list[Token] - созданные токены.
        tokens_count: int - счетчик созданных токенов.
    """

    def __init__(self) -> None:
        """Метод инициализации."""
        self.users: list[User] = []
        self.users_count: int = 0

    def update_user(
        self, vector: list[dict[str, Any]], username: str,
    ) -> User | None:
        """
        Создает пользователя в базе данных.

        Создает, сохраняет в базе данных
        и возвращает индексированную запись о пользователе.

        :param username: Имя пользователя
        :type username: str
        :param vector: Вектор лица пользователя
        :type vector: list[dict[str, Any]]
        :return: индексированная запись о пользователе.
        :rtype: User
        """
        user = User(
            username=username,
            is_verified=True,
            vector=vector,
        )
        user_in_db = self.get_user(user)

        if user_in_db is None:
            user_in_db = self.create_user(user)
            self.users.append(user_in_db)
            self.users_count += 1
            logger.info(f'Created user {user_in_db}')
            return user_in_db

        user_position = self.users.index(user_in_db)
        user.user_id = user_in_db.user_id
        self.users[user_position] = user
        logger.info(f'Updated {user}')
        return user

    def create_user(self, user: User) -> User:
        """
        Создает пользователя в базе данных.

        Создает, сохраняет в базе данных
        и возвращает индексированную запись о пользователе.

        :param user: неидексированная запись о пользователе.
        :type user: User
        :return: индексированная запись о пользователе.
        :rtype: User
        """
        indexed_user = User(
            username=user.username,
            is_verified=True,
            user_id=self.users_count,
        )
        self.users.append(indexed_user)
        self.users_count += 1
        logger.info(f'Created user {indexed_user}')
        return indexed_user

    def get_user(self, user: User) -> User | None:
        """
        Получает пользователя из базы данных.

        Получает и возвращает запись о пользователе из базы данных.

        :param user: неидексированная запись о пользователе.
        :type user: User
        :return: индексированная запись о пользователе.
        :rtype: User
        """
        try:
            in_db_user = [
                member for member in self.users if (
                    member.username == user.username
                )
            ][0]
        except IndexError:
            logger.warning(f'{user} is not found')
            return None

        logger.info(f'got {in_db_user}')
        return in_db_user
