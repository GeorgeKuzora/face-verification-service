import logging
import os
import shutil
from enum import StrEnum
from pathlib import Path

import pytest

from app.service import FaceVerificationService, ModelName

logger = logging.getLogger(__name__)


@pytest.fixture
def tmp_file_valid(tmp_path: Path):
    """Фикстура для создания временного файла изображения."""
    test_data_dir_path = 'src/tests/test_data/'
    test_file_name = 'me.jpg'
    test_file_path = Path(test_data_dir_path + test_file_name)

    if not test_file_path.is_file():
        logger.error(f'file {test_file_path} is not found')
        raise OSError

    tmp_file_path: Path = tmp_path / test_file_name
    if tmp_file_path.is_file():
        os.remove(tmp_file_path)

    tmp_file = shutil.copy(test_file_path, tmp_file_path)
    yield tmp_file
    os.remove(tmp_file)


@pytest.fixture
def tmp_file_not_found():
    """Фикстура для получения неверного пути к файлу."""
    return Path('/invalid_tmp_file_path')


@pytest.fixture
def tmp_file_invalid_filetype():
    """Фикстура для создания файла неверного типа."""
    file_name = 'temp.txt'
    with open(file_name, 'w'):
        ...
    yield file_name
    os.remove(file_name)
