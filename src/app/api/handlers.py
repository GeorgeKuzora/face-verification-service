from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def root_handler() -> dict[str, str]:
    """
    Возвращает сообщение что сервер работает.

    :return: Сообщение
    :rtype: dict[str, str]
    """
    return {'message': 'server is running'}
