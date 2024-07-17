import os
import random
from pathlib import Path

import pytest


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
