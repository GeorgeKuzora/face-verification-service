import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.handlers import router
from app.api.healthz.handlers_healthz import router as healthz_router
from app.core.face_verification import FaceVerificationService
from app.external.kafka import KafkaConsumer
from app.external.postgres.storage import DBStorage
from app.system.runner import AsyncMultiProcessRunner

logger = logging.getLogger(__name__)


def init_kafka() -> KafkaConsumer:
    """Инициализирует KafkaConsumer."""
    logger.info('Starting up storage...')
    storage = DBStorage()
    logger.info('Starting up service...')
    runner = AsyncMultiProcessRunner()
    logger.info('Starting up kafka consumer...')
    service = FaceVerificationService(storage=storage, runner=runner)
    logger.info('Starting up runner...')
    return KafkaConsumer(service=service)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Метод для lifespan events приложения."""
    kafka = init_kafka()
    await kafka.start()
    await kafka.consume()
    yield
    logger.info('Shutting down kafka storage...')
    await kafka.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
app.include_router(router=healthz_router)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
