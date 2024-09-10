import os
import random
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.face_verification import FaceVerificationService, Validator
from app.core.models import User
from app.external.in_memory_storage import InMemoryStorage

test_user = User(username='george', is_verified=False)
invalid_user = User(username='invalid', is_verified=False)
user_list2objects = [
    User(username='george', is_verified=False),
    User(username='peter', is_verified=False),
]


@pytest.fixture
def valid_tmp_file(tmp_path):
    """Фикстура для создания тестового файла."""
    file_id = random.randint(1, 9)  # noqa: S311 randint for test filenames
    file_name = f'temp{file_id}.txt'
    file_path = tmp_path / file_name
    with open(file_path, 'w') as tmp_file:
        tmp_file.write('\n')
    yield file_path
    os.remove(file_path)


@pytest.fixture
def invalid_tmp_file():
    """Фикстура для получения неверного пути к файлу."""
    return Path('/invalid_tmp_file_path')


@pytest.fixture
def service():
    """
    Фикстура создает экземпляр сервиса.

    Атрибуты сервиса repository, config являются mock объектами.

    :return: экземпляр сервиса
    :rtype: AuthService
    """
    storage = MagicMock()
    runner = AsyncMock()
    return FaceVerificationService(storage=storage, runner=runner)


@pytest.fixture
def storage():
    """
    Хранилище данных.

    :return: Хранилище данных
    :rtype: InMemoryStorage
    """
    return InMemoryStorage()


@pytest.fixture
def single_user_in_repo_factory(storage):
    """Фикстура репозитория с одной записью о пользователе."""
    users_in_repo = 1
    storage.create_user(user_list2objects[0])
    return storage, users_in_repo


@pytest.fixture
def two_users_in_repo_factory(storage):
    """Фикстура репозитория с двумя записями о пользователях."""
    users_in_repo = 2
    for user_id in range(users_in_repo):
        storage.create_user(user_list2objects[user_id])
    return storage, users_in_repo


@pytest.fixture
def validator():
    """
    Экземпляр валидатора.

    :return: Экземпляр валидатора.
    :rtype: Validator
    """
    return Validator()
