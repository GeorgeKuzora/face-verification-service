import asyncio
from concurrent.futures import Executor, ProcessPoolExecutor
from functools import partial
from typing import Any, Callable


class AsyncMultiProcessRunner:
    """Раннер для запуска а асинхронной функции в новом процессе."""

    async def run(self, func: Callable[[str, str], Any], **kwargs) -> Any:
        """
        Метод запуска функции.

        :param func: Запускаемая синхронная функция
        :type func: Callable
        :param kwargs: Атрибуты функции
        :type kwargs: key-value pairs
        :return: Результат выполнения
        """
        with ProcessPoolExecutor() as pool:
            return await self._run(pool, func, **kwargs)

    async def _run(
        self, executor: Executor, func: Callable[[str, str], Any], **kwargs,
    ) -> None:
        represent_image_on_path = partial(func, **kwargs)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor,
            represent_image_on_path,
        )
