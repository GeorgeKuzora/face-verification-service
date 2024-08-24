import json
import logging
from datetime import datetime
from pathlib import Path

from aiokafka import AIOKafkaConsumer

from app.core.config import get_settings
from app.core.face_verification import FaceVerificationService

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Очередь сообщений кафка."""

    def __init__(self, service: FaceVerificationService) -> None:
        """Метод инициализации."""
        self.service = service

        self.consumer = AIOKafkaConsumer(
            get_settings().kafka.topics,
            bootstrap_servers=get_settings().kafka.host,
            value_deserializer=self.deserializer,
        )

        self._init_storage_path()

    async def consume(self) -> None:
        """Функция для обработки сообщений kafka."""
        while True:  # noqa: WPS457 kafka running
            async for msg in self.consumer:
                message: dict[str, str] = msg.value  # type: ignore
                username = message.get('username', '')
                img_path = message.get('file_path', '')
                await self.service.verify(username=username, img_path=img_path)

    async def start(self) -> None:
        """Запускает consumer."""
        await self.consumer.start()

    async def stop(self) -> None:
        """Останавливает consumer."""
        await self.consumer.stop()

    def deserializer(self, serialized: bytes) -> dict[str, str]:
        """
        Десериализирует сообщение после получения в kafra.

        :param serialized: Сериализованное значение сообщения.
        :type serialized: bytes
        :return: Десериализованное сообщение.
        :rtype: dict[str, str]
        """
        return json.loads(serialized)  # type: ignore

    def _init_storage_path(self) -> None:
        path = Path(get_settings().kafka.storage_path)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            raise OSError(f'{path} is already exists and not a directory')

    def _get_file_path(self, username) -> str:
        """Создает уникальный путь к файлу пользователя."""
        file_upload_timestamp = datetime.now().isoformat()
        filename = f'{username}-{file_upload_timestamp}'
        file_storage_path = get_settings().kafka.storage_path
        return f'{file_storage_path}/{filename}'
