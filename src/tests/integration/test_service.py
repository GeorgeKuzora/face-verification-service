import pytest

from app.external.kafka import KafkaConsumer
from app.service import init_kafka


@pytest.mark.asyncio
@pytest.mark.anyio
async def test_init_kafka():
    """Тестирует функцию init_kafka."""
    kafka = init_kafka()

    assert isinstance(kafka, KafkaConsumer)
