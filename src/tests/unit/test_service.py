import os
import random
from enum import StrEnum
from pathlib import Path

import pytest

from app.service import FaceVerificationService, ModelName


@pytest.fixture
def valid_tmp_file(tmp_path):
    """Фикстура для создания тестового файла."""
    file_id = random.randint(1, 9)
    file_name = f'temp{file_id}.txt'
    with open(file_name, 'w'):
        ...
    file_path = tmp_path / file_name
    yield file_path
    os.remove(file_path)
