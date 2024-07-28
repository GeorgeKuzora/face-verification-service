import pytest

from app.external.in_memory_storage import InMemoryStorage


@pytest.fixture
def storage():
    """Фикстура для создания объекта InMemoryRepository."""
    return InMemoryStorage()
