import logging
from enum import StrEnum
from pathlib import Path
from typing import Any

from deepface import DeepFace

logger: logging.Logger = logging.getLogger(__name__)


class ModelName(StrEnum):
    """
    Названия подерживаемых моделей распознавания лиц.

    Attributes:
        attribute_name: type and description.
    """

    facenet = 'Facenet'


class FaceVerificationService:
    """
    Сервис распознавания лица.

    Служит для вызова функций библиотеки распознавания лица DeepFace.

    Attributes:
        verificator: Библиотека распознавания лица. По умолчанию DeepFace
    """

    def __init__(self, library: object = DeepFace) -> None:
        """
        Функция инициализации.

        Args:
            library: Библиотека для распознавания лиц.
        """
        self.library = library

    def represent(
        self, img_path: str | Path, model_name: str = ModelName.facenet,
    ) -> list[dict[str, Any]]:
        """
        Служит для получения представления изображения в виде списка векторов.

        Возвращает список вложенных векторов.

        Args:
            img_path: str | pathlib.Path, путь к файлу изображения
            model_name: ModelName, название модели анализа изображения

        Returns:
            list[dict[str, Any]]: Список вложенных векторов

        Raises:
            ValueError: Возвращает ошибку значения при передаче
              невалидных значений пути, имени модели или ошибке
              в библиотеке анализа изображений
        """
        self._validate_path(img_path)
        self._validate_model_name(model_name)
        img_path = str(img_path)
        return self._get_representation(img_path, model_name)

    def _validate_path(self, path) -> None:
        if not self._is_path(path):
            logger.error(f"file {path} doesn\'t extist")
            raise ValueError(f"file {path} doesn\'t extist")

    def _is_path(self, path: str | Path) -> bool:
        if isinstance(path, str):
            path = Path(path)
        return path.is_file()

    def _validate_model_name(self, model_name) -> None:
        if not self._is_model_name(model_name):
            logger.error(f"model {model_name} isn\'t supported")
            raise ValueError(f"model {model_name} isn\'t supported")

    def _is_model_name(self, model_name: ModelName) -> bool:
        model_name_values: list[str] = [member.value for member in ModelName]
        return model_name.value in model_name_values

    def _get_representation(
        self, img: str, model_name: str,
    ) -> list[dict[str, Any]]:
        try:
            embedding_objs: list[dict[str, Any]] = DeepFace.represent(
                img_path=img,
                model_name=model_name,
            )
        except ValueError as err:
            logger.error(
                'unexpected exception in a face verification library',
                exc_info=True,
            )
            raise ValueError(
                'unexpected exception in a face verification library',
            ) from err
        return embedding_objs
