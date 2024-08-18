from fastapi import HTTPException, status


class ServerError(HTTPException):
    """Ошибка при проблемах с сервисом."""

    def __init__(
        self,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail: str = 'Неизвестная ошибка сервера',
    ):
        """
        Метод инициализации ServerError.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail


class StorageError(ServerError):
    """
    Исключение возникающее при запросе в хранилище данных.

    Импортировать в имплементации репозитория данных,
    для вызова исключения при ошибке доступа к данным.
    """


class ConfigError(ServerError):
    """
    Исключение возникающее в ходе конфигурации.

    Импортировать в имплементации репозитория данных,
    для вызова исключения при ошибке доступа к данным.
    """
