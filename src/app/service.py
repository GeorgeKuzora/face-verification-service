import logging
from enum import StrEnum

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
