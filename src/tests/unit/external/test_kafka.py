import pytest

from app.core.models import Message
from app.external.kafka import Kafka


@pytest.mark.asyncio
async def test_get_message():
    """Тестирует метод get_message."""
    kafka = Kafka()

    message = await kafka.get_message()
    assert message
    assert isinstance(message, Message)
