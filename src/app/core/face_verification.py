import asyncio
import logging
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Protocol

from deepface import DeepFace

from app.core.errors import StorageError
from app.core.models import User

logger: logging.Logger = logging.getLogger(__name__)


class Runner(Protocol):
    """Класс запуска функций в различных режимах."""

    async def run(self, func: Callable[[str, str], Any], **kwargs) -> Any:
        """
        Метод запуска функции.

        :param func: Запускаемая функция
        :type func: Callable
        :param kwargs: Атрибуты функции в форме ключ-значение
        :type kwargs: key-value pairs
        """
        ...  # noqa: WPS428 default Protocol syntax


class Storage(Protocol):
    """
    Интерфейс для работы с хранилищами данных.

    Repository - это слой абстракции для работы с хранилищами данных.
    Служит для уменьшения связности компонентов сервиса.
    """

    def update_user(
        self, vector: list[dict[str, Any]], username: str,
    ) -> User | None:
        """
        Абстрактный метод обновления пользователя.

        :param username: Имя пользователя
        :type username: str
        :param vector: Вектор лица пользователя
        :type vector: list[dict[str, Any]]
        """
        ...  # noqa: WPS428 default Protocol syntax


class ModelName(StrEnum):
    """
    Названия поддерживаемых моделей распознавания лиц.

    Attributes:
        attribute_name: type and description.
    """

    facenet = 'Facenet'


class Validator:
    """Класс валидации данных сервиса."""

    def validate_path(self, path: Path | str) -> None:
        """
        Валидирует путь.

        :param path: Путь.
        :type path: Path
        :raises ValueError: При ошибке доступа к файлу
        """
        if not self._is_path(path):
            logger.error(f"file {path} doesn\'t exist")
            raise ValueError(f"file {path} doesn\'t exist")

    def validate_model_name(self, model_name: ModelName | str) -> None:
        """
        Валидирует имя модели.

        :param model_name: Имя модели.
        :type model_name: ModelName
        :raises ValueError: При ошибке имени модели
        """
        if not self._is_model_name(model_name):
            logger.error(f"model {model_name} isn\'t supported")
            raise ValueError(f"model {model_name} isn\'t supported")

    def _is_path(self, path: str | Path) -> bool:
        if isinstance(path, str):
            path = Path(path)
        return path.is_file()

    def _is_model_name(self, model_name: ModelName | str) -> bool:
        model_name_values: list[str] = [member.value for member in ModelName]
        if not isinstance(model_name, ModelName):
            return model_name in model_name_values
        return model_name.value in model_name_values


def _represent(img_path: str, model_name: str) -> Any:
    return DeepFace.represent(
        img_path=img_path,
        model_name=model_name,
    )


class FaceVerificationService:
    """
    Сервис распознавания лица.

    Служит для вызова функций библиотеки распознавания лица DeepFace.
    """

    def __init__(
        self, storage: Storage, runner: Runner, library: type = DeepFace,
    ) -> None:
        """
        Функция инициализации.

        :param storage: Хранилище данных
        :type storage: Storage
        :param runner: Обработчик функции
        :type runner: Runner
        :param library: Библиотека для распознавания лиц, defaults to DeepFace.
        :type library: type
        """
        self.storage = storage
        self.library = library
        self.validator = Validator()
        self.runner = runner

    async def verify(self, username: str, img_path: str) -> None:
        """
        Верифицирует пользователя.

        Получает вектор изображения пользователя.
        Верифицирует пользователя.
        Удаляет использованное изображение пользователя.

        :param username: Имя пользователя
        :type username: str
        :param img_path: Путь к изображению пользователя
        :type img_path: str
        """
        try:
            vector = await self.represent(img_path=img_path)
        except ValueError:
            logger.error(f"can't get vector for {username}")
            task = asyncio.create_task(self._delete_path(img_path))
            await task
            return
        logger.info(f'got vector {vector} for {username}')
        delete_task = asyncio.create_task(self._delete_path(img_path))
        update_user_task = asyncio.create_task(
            self.update_user(vector, username),
        )
        try:
            await asyncio.gather(delete_task, update_user_task)
        except Exception:
            logger.error(f"can't update {username}")

    async def represent(
        self, img_path: str | Path, model_name: str = ModelName.facenet,
    ) -> Any:
        """
        Служит для получения представления изображения в виде списка векторов.

        Возвращает список вложенных векторов.

        :param img_path: путь к файлу изображения
        :type img_path: str | pathlib.Path
        :param model_name: ModelName, название модели анализа изображения
        :type model_name: str
        :return: Список вложенных векторов
        :rtype: list[dict[str, Any]]
        """
        self.validator.validate_path(img_path)
        self.validator.validate_model_name(model_name)
        img_path = str(img_path)
        return await self.runner.run(
            _represent, img_path=img_path, model_name=model_name,
        )

    async def update_user(
        self, vector: list[dict[str, Any]], username: str,
    ) -> None:
        """
        Обновляет данные пользователя в базе данных.

        :param vector: Вектор лица пользователя
        :type vector: list[dict[str, Any]]
        :param username: Имя пользователя
        :type username: str
        :raises StorageError: При ошибке в базе данных
        """
        user: User | None = self.storage.update_user(vector, username)
        if not user:
            logger.error('StorageError: user is not updated')
            raise StorageError(detail='error in storage, user is not updated')

    async def _delete_path(self, img_path: str) -> None:
        path = Path(img_path)
        try:
            self.validator.validate_path(img_path)
        except ValueError:
            logger.warning(f'{img_path} not found, can not remove')
        else:
            path.unlink()
