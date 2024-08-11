import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.handlers import router
from app.core.face_verification import FaceVerificationService
from app.external.in_memory_storage import InMemoryStorage
from app.external.kafka import KafkaConsumer
from app.system.runner import AsyncMultiProccessRunner

logger = logging.getLogger(__name__)


def _init_kafka() -> KafkaConsumer:
    logger.info('Starting up storage...')
    storage = InMemoryStorage()
    logger.info('Starting up service...')
    runner = AsyncMultiProccessRunner()
    logger.info('Starting up kafka consumer...')
    service = FaceVerificationService(storage=storage, runner=runner)
    logger.info('Starting up runner...')
    return KafkaConsumer(service=service)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Метод для lifespan events приложения."""
    kafka = _init_kafka()
    await kafka.start()
    await kafka.consume()
    yield
    logger.info('Shutting down kafka storage...')
    await kafka.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
