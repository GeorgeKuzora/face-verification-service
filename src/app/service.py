import logging

from deepface import DeepFace



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
