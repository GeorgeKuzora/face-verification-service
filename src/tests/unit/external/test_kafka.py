import json
from pathlib import Path
from unittest.mock import AsyncMock

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
        """Тестирует что данные десериализируются корректно."""
        deserialized_data = consumer.deserializer(serialized_data)

        assert deserialized_data == self.test_data


class TestInitStoragePath:
    """Тестирует метод _init_storage_path."""

    @pytest.fixture
    def path(self):
        """Фикстура для получения и очистки пути."""
        path = Path(get_settings().kafka.storage_path)
        try:
            yield path
        finally:
            path.rmdir()

    @pytest.fixture
    def path_is_forbidden(self):
        """Фикстура для получения и очистки занятого пути."""
        path = Path(get_settings().kafka.storage_path)
        path.rmdir()
        path.touch()
        try:  # noqa: WPS501 need for cleaning after test
            yield path
        finally:
            path.unlink()

    def test_init_storage_path(self, consumer: KafkaConsumer, path: Path):
        """Тестирует что директория была создана."""
        consumer._init_storage_path()
        assert path.is_dir()

    def test_init_storage_path_raises(
        self, consumer: KafkaConsumer, path_is_forbidden: Path,
    ):
        """Тестирует что директория была создана."""
        with pytest.raises(OSError):
            consumer._init_storage_path()


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
        """Тестирует что file_path уникален и содержит путь к директории."""
        file_path_before = consumer._get_file_path(self.test_username)
        file_path_after = consumer._get_file_path(self.test_username)

        assert file_storage_path in file_path_before
        assert file_storage_path in file_path_after
        assert file_path_before != file_path_after


class TestStartStop:
    """Тестирует методы start и stop."""

    @pytest.fixture
    def consumer_mock(self, consumer: KafkaConsumer):
        """Мок методов start и стоп у клиента AIOKafkaConsumer."""
        consumer.consumer.start = AsyncMock()
        consumer.consumer.stop = AsyncMock()
        return consumer

    @pytest.mark.asyncio
    @pytest.mark.anyio
    async def test_start_stop(self, consumer_mock: KafkaConsumer):
        """Тестирует что методы выполняются."""
        await consumer_mock.start()
        await consumer_mock.stop()

        consumer_mock.consumer.start.assert_awaited_once()
        consumer_mock.consumer.stop.assert_awaited_once()
