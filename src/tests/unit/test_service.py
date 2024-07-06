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


@pytest.fixture
def invalid_tmp_file():
    """Фикстура для получения неверного пути к файлу."""
    return Path('/invalid_tmp_file_path')


@pytest.mark.parametrize(
    'path, expected',
    (
        pytest.param('valid_tmp_file', True, id='is_valid_path'),
        pytest.param('invalid_tmp_file', False, id='is_invalid_path'),
    ),
)
def test_is_path(path, expected, request) -> None:
    """Тестирует метод FaceVerificationService._is_path."""
    path = request.getfixturevalue(path)
    service = FaceVerificationService()
    assert service._is_path(path) == expected  # noqa: WPS437


@pytest.mark.parametrize(
    'path',
    (
        pytest.param('valid_tmp_file', id='is_valid_path'),
        pytest.param(
            'invalid_tmp_file',
            id='is_invalid_path',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ),
)
def test_validate_path(path: Path, request) -> None:
    """Тестирует метод FaceVerificationService._validate_path."""
    path = request.getfixturevalue(path)
    service = FaceVerificationService()
    service._validate_path(path)  # noqa: WPS437


class InvalidModel(StrEnum):
    """Неверная модель."""

    invalid_model = 'Invalid_model'


@pytest.mark.parametrize(
    'model_name, expected',
    (
        pytest.param(ModelName.facenet, True, id='Facenet'),
        pytest.param(
            InvalidModel.invalid_model,
            False,
            id='invalid_model_name',
        ),
    ),
)
def test_is_model_name(model_name, expected, request) -> None:
    """Тестирует метод FaceVerificationService._is_model_name."""
    service = FaceVerificationService()
    assert service._is_model_name(model_name) == expected  # noqa: WPS437


@pytest.mark.parametrize(
    'model_name',
    (
        pytest.param(ModelName.facenet, id='Facenet'),
        pytest.param(
            InvalidModel.invalid_model,
            id='invalid_model_name',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ),
)
def test_validate_model_name(model_name):
    """Тестирует метод FaceVerificationService._validate_model_name."""
    service = FaceVerificationService()
    service._validate_model_name(model_name)  # noqa: WPS437


class TestRepresent:
    """Класс для тестирования метода FaceVerificationService.represent."""

    mock_deepface_representation = [{'face': 123}]
