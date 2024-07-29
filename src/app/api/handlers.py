import asyncio
from concurrent.futures import Executor, ProcessPoolExecutor
from typing import Annotated, Any, Callable

from fastapi import Depends

from app.core.face_verification import FaceVerificationService
from app.core.models import Message
from app.external.in_memory_storage import InMemoryStorage
from app.external.kafka import Kafka
from fastapi import APIRouter

router = APIRouter()

async def run_in_executor(executor: Executor, func: Callable[[], Any]) -> Any:
    """
    Запускает функцию в эксекъюторе.

    :param executor: Эксекютор
    :type executor: Executor
    :param func: Вызываемая функция
    :type func: Callable
    :return: Результат выполнения функции
    :rtype: Any
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func)


async def update_user(
    executor: Executor, message: Message, service: FaceVerificationService,
) -> None:
    """
    Функция обновления пользователя.

    Служит для вызова обновления пользователя в отдельном процессе.

    :param executor: Эксекютор
    :type executor: Executor
    :param message: Сообщение с информацией для обновления
    :type message: Message
    :param service: Объект сервиса
    :type service: FaceVerificationService
    """
    get_vector_task = asyncio.create_task(service.represent(message.path))
    face_vector = await get_vector_task
    await asyncio.gather(
        run_in_executor(
            executor,
            lambda: service.update_user(face_vector, message.username),
        ),
    )


@router.get('/')
async def root_handler() -> dict[str, str]:
    """
    Возращает сообщение что сервер работает.

    :return: Сообщение
    :rtype: dict[str, str]
    """
    return {'message': 'server is running'}


def get_service():
    """
    Возвращает экземляр сервиса.

    :return: Экземляр сервиса
    :rtype: FaceVerificationService
    """
    storage = InMemoryStorage()
    return FaceVerificationService(storage)


def get_kafka():
    """
    Возвращает экземляр kafka.

    :return: Экземляр kafka
    :rtype: Kafka
    """
    return Kafka()


@router.post('/kafka')
async def verify(
    service: Annotated[FaceVerificationService, Depends(get_service)],
    kafka: Annotated[Kafka, Depends(get_kafka)],
) -> dict[str, str]:
    """
    Верифицирует пользователя.

    :param service: Экземпляр сервиса
    :type service: FaceVerificationService
    :param kafka: Экземпляр kafka
    :type kafka: Kafka
    :return: Сообщение
    :rtype: dict[str, str]
    """
    get_message_task = asyncio.create_task(kafka.get_message())
    message = await get_message_task
    with ProcessPoolExecutor() as pool:
        asyncio.run(
            update_user(pool, message, service),
        )
    return {'message': 'ok'}
