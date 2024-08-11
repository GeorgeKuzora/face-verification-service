import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Self

import yaml
from pydantic_settings import BaseSettings

from app.core.errors import ConfigError

logger = logging.getLogger(__name__)


class KafkaSettings(BaseSettings):
    """Конфигурация kafka producer."""

    host: str
    port: int
    file_encoding: str = 'utf-8'
    file_compression_quality: int = 1
    storage_path: str
    topics = str

    @property
    def instance(self) -> str:
        """
        Свойство для получения адреса kafka.

        :return: Адрес kafka
        :rtype: str
        :raises ConfigError: При ошибке конфигурации сервиса
        """
        return f'{self.host}:{self.port}'


class Settings(BaseSettings):
    """Конфигурация приложения."""

    kafka: KafkaSettings

    @classmethod
    def from_yaml(cls, config_path) -> Self:
        """Создает объект класса из файла yaml."""
        if not cls._is_valid_path(config_path):
            logger.critical(
                f'config file is missing on path {config_path}',
            )
            raise ConfigError(
                detail=f'config file is missing on path {config_path}',
            )
        settings = yaml.safe_load(Path(config_path).read_text())
        return cls(**settings)

    @classmethod
    def _is_valid_path(cls, path: str) -> bool:
        passlib_path = Path(path)
        return passlib_path.is_file()


@lru_cache
def get_settings() -> Settings:
    """Создает конфигурацию сервиса."""
    config_path_env_var = 'CONFIG_PATH'
    config_file = os.getenv(config_path_env_var)
    return Settings.from_yaml(config_file)
