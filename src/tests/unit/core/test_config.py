import os
from enum import StrEnum

import pytest
from pydantic import ValidationError

from app.core.config import KafkaSettings, Settings, get_settings
from app.core.errors import ConfigError


class Key(StrEnum):
    """Часто используемые строки."""

    host = 'host'
    port = 'port'
    file_encoding = 'file_encoding'
    file_compression_quality = 'file_compression_quality'
    storage_path = 'storage_path'
    topics = 'topics'
    kafka = 'kafka'


kafka_valid_input = {
    Key.host: 'kafka',
    Key.port: 9092,
    Key.file_encoding: 'utf-8',
    Key.file_compression_quality: 1,
    Key.storage_path: '/src/config.yml',
    Key.topics: 'faces',
}

kafka_invalid_input = {
    Key.port: 'not_int',
    Key.file_encoding: 'utf-8',
    Key.file_compression_quality: 1,
    Key.storage_path: '/src/config.yml',
    Key.topics: 'faces',
}

valid_input = {Key.kafka: kafka_valid_input}
invalid_input = {Key.kafka: kafka_invalid_input}
valid_config_path = 'src/config/config-local.yml'
invalid_config_path = 'src/config/invalid_path.yml'


class TestKafkaSettings:
    """Тестирует класс KafkaSettings."""

    @pytest.mark.parametrize(
        'input_values', (
            pytest.param(
                kafka_valid_input,
                id='valid input parameters',
            ),
            pytest.param(
                kafka_invalid_input,
                id='invalid input parameters',
                marks=pytest.mark.xfail(raises=ValidationError),
            ),
        ),
    )
    def test_init(self, input_values: dict):
        """Тестирует инициализацию класса."""
        settings = KafkaSettings(**input_values)
        expected_host = input_values[Key.host]
        expected_port = input_values[Key.port]
        expected_instance = f'{expected_host}:{expected_port}'

        assert settings.host == expected_host
        assert settings.port == expected_port
        assert settings.instance == expected_instance


class TestSettings:
    """Тестирует класс Settings."""

    @pytest.mark.parametrize(
        'input_values', (
            pytest.param(
                valid_input,
                id='valid input parameters',
            ),
            pytest.param(
                invalid_input,
                id='invalid input parameters',
                marks=pytest.mark.xfail(raises=ValidationError),
            ),
        ),
    )
    def test_init(self, input_values: dict):
        """Тестирует инициализацию класса."""
        settings = Settings(**input_values)

        assert settings.kafka.host == input_values[Key.kafka][Key.host]  # type: ignore  # noqa: E501
        assert settings.kafka.port == input_values[Key.kafka][Key.port]  # type: ignore  # noqa: E501

    @pytest.mark.parametrize(
        'config_path', (
            pytest.param(
                valid_config_path,
                id='valid config path',
            ),
            pytest.param(
                invalid_config_path,
                id='invalid config path',
                marks=pytest.mark.xfail(raises=ConfigError),
            ),
        ),
    )
    def test_from_yml(self, config_path):
        """Тестирует метод from_yaml."""
        settings = Settings.from_yaml(config_path)

        assert settings.kafka.host == valid_input[Key.kafka][Key.host]  # type: ignore  # noqa: E501
        assert settings.kafka.port == valid_input[Key.kafka][Key.port]  # type: ignore  # noqa: E501


@pytest.fixture
def valid_config_path_env():
    """Устанавливает валидный путь в переменной окружения."""
    os.environ['CONFIG_PATH'] = valid_config_path
    return valid_config_path


@pytest.mark.parametrize(
    'config_file_path', (
        pytest.param(
            'valid_config_path_env',
            id='valid config file path',
        ),
    ),
)
def test_get_settings(config_file_path, request):
    """Тестирует функцию get_settings."""
    request.getfixturevalue(config_file_path)

    settings = get_settings()

    assert settings.kafka.host == valid_input[Key.kafka][Key.host]  # type: ignore  # noqa: E501
    assert settings.kafka.port == valid_input[Key.kafka][Key.port]  # type: ignore  # noqa: E501
