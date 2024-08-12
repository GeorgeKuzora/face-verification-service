import json
from pathlib import Path

import pytest
import pytest_asyncio

from app.core.config import get_settings
from app.external.kafka import KafkaConsumer


@pytest_asyncio.fixture
async def consumer(service):
    """Создает KafkaConsumer."""
    return KafkaConsumer(service)


class TestDeserializer:
    """Тестирует метод deserializer."""

    test_data = {'username': 'george', 'file_path': '/var/image.png'}

    @pytest.fixture
    def serialized_data(self):
        """Сериализованные данные."""
        return json.dumps(self.test_data).encode()

    @pytest.mark.asyncio
    async def test_deserializer(self, consumer: KafkaConsumer, serialized_data):
        """Тестирует что данные десериализируются коректно."""
        deserialized_data = consumer.deserializer(serialized_data)

        assert deserialized_data == self.test_data


class TestInitStaragePath:
    """Тестирует метод _init_storage_path."""

    @pytest.fixture
    def path(self):
        """Фикстура для получения и очистки пути."""
        path = Path(get_settings().kafka.storage_path)
        try:
            yield path
        finally:
            path.rmdir()

    def test_init_storage_path(self, consumer: KafkaConsumer, path: Path):
        """Тестирует что директория была создана."""
        consumer._init_storage_path()
        assert path.is_dir()


class TestGetFilePath:
    """Тестирует метод _get_file_path."""

    test_username = 'george'

    @pytest.fixture
    def file_storage_path(self):
        """Фикстура для получения пути к векторам."""
        return str(Path(get_settings().kafka.storage_path))

    def test_get_file_path(
        self, consumer: KafkaConsumer, file_storage_path: str,
    ):
        """Тестрирует что file_path уникален и содержит путь к директории."""
        file_path_before = consumer._get_file_path(self.test_username)
        file_path_after = consumer._get_file_path(self.test_username)

        assert file_storage_path in file_path_before
        assert file_storage_path in file_path_after
        assert file_path_before != file_path_after
