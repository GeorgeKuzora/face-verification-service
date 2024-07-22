import logging
from pathlib import Path

from app.core.models import Message

logger = logging.getLogger(__name__)


class Kafka:
    """Очередь сообщений кафка."""

    async def get_message(self) -> Message:
        """
        Получает сообщение из очереди.

        :return: Сообщение для работы
        :rtype: Message
        :raises OSError: Если файл не найден
        """
        data_dir_path = 'src/tests/test_data/'
        file_name = 'me.jpg'
        file_path = Path(data_dir_path + file_name)
        if not file_path.is_file():
            logger.error(f'file {file_path} is not found')
            raise OSError
        username = 'george'
        return Message(username=username, path=file_path)
