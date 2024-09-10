import logging
import os
import shutil
from enum import StrEnum
from pathlib import Path

import pytest

from app.core.face_verification import FaceVerificationService, ModelName

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
    try:
        os.remove(tmp_file)
    except Exception:
        logger.info("can't remove file")


@pytest.fixture
def tmp_file_not_found():
    """Фикстура для получения неверного пути к файлу."""
    return Path('/invalid_tmp_file_path')


@pytest.fixture
def tmp_file_invalid_filetype():
    """Фикстура для создания файла неверного типа."""
    file_name = 'temp.txt'
    with open(file_name, 'w') as invalid_type_file:
        invalid_type_file.write('\n')
    yield file_name
    try:
        os.remove(file_name)
    except Exception:
        logger.info("can't remove file")


class InvalidModel(StrEnum):
    """Неверная модель пользователя."""

    invalid_model = 'Invalid_model'


test_vector_min_length = 1


@pytest.fixture
def service(storage, runner):
    """
    Объект сервиса.

    :param storage: Хранилище данных
    :type storage: Storage
    :param runner: Раннер функции
    :type runner: Runner
    :return: Экземпляр сервиса
    :rtype: FaceVerificationService
    """
    return FaceVerificationService(storage=storage, runner=runner)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'path, model_name, vector_min_lenght',
    (
        pytest.param(
            'tmp_file_valid',
            ModelName.facenet,
            test_vector_min_length,
            id='valid file, valid model',
            marks=pytest.mark.slow,
        ),
        pytest.param(
            'tmp_file_valid',
            InvalidModel.invalid_model,
            None,
            id='valid file, invalid model name',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            'tmp_file_not_found',
            ModelName.facenet,
            None,
            id='file not found, valid model name',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            'tmp_file_invalid_filetype',
            ModelName.facenet,
            None,
            id='invalid filetype, valid model name',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            'tmp_file_not_found',
            InvalidModel.invalid_model,
            None,
            id='invalid path, invalid model name',
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ),
)
async def test_represent(
    path,
    model_name,
    vector_min_length,
    request,
    service,
):
    """Тестирует метод FaceVerificationService.represent."""
    path = request.getfixturevalue(path)

    vector = await service.represent(path, model_name)
    vector_length = len(vector)

    assert vector_length >= vector_min_length


class TestVerify:
    """Тестирует метод verify."""

    yes = True
    nope = False
    words_in_vector_log = [
        'embedding', 'facial_area', 'left_eye', 'right_eye', 'face_confidence',
    ]

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'path, got_vector',
        (
            pytest.param(
                'tmp_file_valid',
                yes,
                id='valid file, valid model',
                marks=pytest.mark.slow,
            ),
            pytest.param(
                'tmp_file_not_found',
                nope,
                id='file not found, valid model name',
            ),
            pytest.param(
                'tmp_file_invalid_filetype',
                nope,
                id='invalid filetype, valid model name',
            ),
        ),
    )
    async def test_verify(  # noqa: WPS211 need for setting test states
        self,
        path,
        got_vector,
        request,
        service,
        caplog,
    ):
        """Тестирует метод verify."""
        caplog.set_level(logging.INFO)
        path = request.getfixturevalue(path)

        await service.verify('george', path)

        if got_vector:
            for word in self.words_in_vector_log:
                assert word in caplog.text
        elif not got_vector:
            for wrd in self.words_in_vector_log:
                assert wrd not in caplog.text
