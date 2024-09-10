import pytest

from app.external.in_memory_storage import InMemoryStorage
from app.system.runner import AsyncMultiProcessRunner


@pytest.fixture
def storage():
    """Фикстура для создания объекта InMemoryRepository."""
    return InMemoryStorage()


@pytest.fixture
def runner():
    """Фикстура для создания объекта InMemoryRepository."""
    return AsyncMultiProcessRunner()
