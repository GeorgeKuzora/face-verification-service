from enum import StrEnum
from pathlib import Path

import pytest

from app.core.face_verification import FaceVerificationService, ModelName


class Fixtures(StrEnum):
    """Названия фикстур."""

    valid_file = 'valid_tmp_file'
    invalid_file = 'invalid_tmp_file'


class TestPathValidation:
    """Тестирует медоды валидации пути."""

    is_valid_path = True
    is_invalid_path = False

    @pytest.mark.parametrize(
        'path, expected',
        (
            pytest.param(
                Fixtures.valid_file, is_valid_path, id='is_valid_path',
            ),
            pytest.param(
                Fixtures.invalid_file, is_invalid_path, id='is_invalid_path',
            ),
        ),
    )
    def test_is_path(self, path, expected, request) -> None:
        """Тестирует метод FaceVerificationService._is_path."""
        path = request.getfixturevalue(path)
        service = FaceVerificationService()
        assert service._is_path(path) == expected

    @pytest.mark.parametrize(
        'path',
        (
            pytest.param(Fixtures.valid_file, id='is_valid_path'),
            pytest.param(
                Fixtures.invalid_file,
                id='is_invalid_path',
                marks=pytest.mark.xfail(raises=ValueError),
            ),
        ),
    )
    def test_validate_path(self, path: Path, request) -> None:
        """Тестирует метод FaceVerificationService._validate_path."""
        path = request.getfixturevalue(path)
        service = FaceVerificationService()
        service._validate_path(path)


class InvalidModel(StrEnum):
    """Неверная модель."""

    invalid_model = 'Invalid_model'


class TestModelValidation:
    """Тестирует методы валидации модели."""

    is_valid_model = True
    is_invalid_model = False

    @pytest.mark.parametrize(
        'model_name, expected',
        (
            pytest.param(ModelName.facenet, is_valid_model, id='Facenet'),
            pytest.param(
                InvalidModel.invalid_model,
                is_invalid_model,
                id='invalid_model_name',
            ),
        ),
    )
    def test_is_model_name(self, model_name, expected) -> None:
        """Тестирует метод FaceVerificationService._is_model_name."""
        service = FaceVerificationService()
        assert service._is_model_name(model_name) == expected

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
    def test_validate_model_name(self, model_name):
        """Тестирует метод FaceVerificationService._validate_model_name."""
        service = FaceVerificationService()
        service._validate_model_name(model_name)


class TestRepresent:
    """Класс для тестирования метода FaceVerificationService.represent."""

    mock_deepface_representation = [{'face': 123}]

    @pytest.fixture
    def mock_deep_face_represent(self, monkeypatch):
        """
        Фикстура для патча метода DeepFace.represent.

        Заменяет возвращаемое значение метода.

        :param monkeypatch: модуль для мокирования
        """
        monkeypatch.setattr(
            'app.core.face_verification.DeepFace.represent',
            lambda img_path, model_name: self.mock_deepface_representation,
        )

    @pytest.fixture
    def mock_deep_face_represent_raises(self, monkeypatch):
        """
        Фикстура для патча метода DeepFace.represent.

        Вызывает ValueError при вызове метода.

        :param monkeypatch: модуль для мокирования
        """
        def raise_value_error(img_path, model_name):  # noqa: WPS430 closure
            raise ValueError

        monkeypatch.setattr(
            'app.core.face_verification.DeepFace.represent',
            raise_value_error,
        )

    def test_get_representation(
        self, valid_tmp_file, mock_deep_face_represent,
    ):
        """
        Тестирует метод FaceVerificationService._get_representation.

        Ожидается что метод вернет значение возвращенное пропатченым
        методом DeepFace.represent.

        :param valid_tmp_file: фикстура правильного файла
        :param mock_deep_face_represent: фикстура для мока метода represent
        """
        service = FaceVerificationService(valid_tmp_file)

        file_path = str(valid_tmp_file)
        assert service._get_representation(  # noqa: WPS437
            file_path, ModelName.facenet,
        ) == self.mock_deepface_representation

    def test_get_representation_raises(
        self,
        valid_tmp_file,
        mock_deep_face_represent_raises,
    ):
        """
        Тестирует метод FaceVerificationService._get_representation.

        Ожидается что метод вызовет ValueError если пропатченый
        метод DeepFace.represent вызывает исключение ValueError.

        :param valid_tmp_file: фикстура правильного файла
        :param mock_deep_face_represent_raises: фикстура для мока
            метода represent

        """
        service = FaceVerificationService(valid_tmp_file)
        file_path = str(valid_tmp_file)

        with pytest.raises(expected_exception=ValueError):
            service._get_representation(
                file_path, ModelName.facenet,
            )

    @pytest.mark.parametrize(
        'path, model_name, expected',
        (
            pytest.param(
                Fixtures.valid_file,
                ModelName.facenet,
                mock_deepface_representation,
                id='valid path, valid model',
            ),
            pytest.param(
                Fixtures.valid_file,
                InvalidModel.invalid_model,
                None,
                id='valid path, invalid model name',
                marks=pytest.mark.xfail(raises=ValueError),
            ),
            pytest.param(
                Fixtures.invalid_file,
                ModelName.facenet,
                None,
                id='invalid path, valid model name',
                marks=pytest.mark.xfail(raises=ValueError),
            ),
            pytest.param(
                Fixtures.invalid_file,
                InvalidModel.invalid_model,
                None,
                id='invalid path, invalid model name',
                marks=pytest.mark.xfail(raises=ValueError),
            ),
        ),
    )
    def test_represent(  # noqa: WPS211 has a lot of params for readability
        self,
        path,
        model_name,
        expected,
        mock_deep_face_represent,
        request,
    ):
        """
        Тестирует метод FaceVerificationService.represent.

        :param path: путь к файлу изображения
        :param model_name: имя модели
        :param expected: ожидаемое значение
        :param mock_deep_face_represent: фикстура для мока метода represent
        :param request: служебный параметр запроса
        """
        path = request.getfixturevalue(path)
        service = FaceVerificationService()

        assert service.represent(path, model_name) == expected

    def test_represent_raises_on_library_error(
        self,
        valid_tmp_file,
        mock_deep_face_represent_raises,
    ):
        """
        Тестирует метод FaceVerificationService.represent.

        Ожидается что метод вызовет ValueError если пропатченый
        метод DeepFace.represent вызывает исключение ValueError.

        :param valid_tmp_file: фикстура правильного файла
        :param mock_deep_face_represent_raises: фикстура для мока
            метода represent
        """
        service = FaceVerificationService()
        with pytest.raises(ValueError):
            service.represent(
                valid_tmp_file, ModelName.facenet,
            )
