import asyncio
from functools import partial
from concurrent.futures import Executor, ProcessPoolExecutor
from typing import Any, Callable


class AsyncMultiProccessRunner:
    """Раннер для запуска а асинхронной функции в новом процессе."""

    async def run(self, func: Callable, img_path: str) -> Any:
        """
        Метод запуска функции.

        :param func: Запускаемая синхронная функция
        :type func: Callable
        :param args: Атрибуты функции
        :type args: key-value pairs
        :return: Результат выполнения
        """
        with ProcessPoolExecutor() as pool:
            return await self._run(pool, func, img_path)

    async def _run(
        self, executor: Executor, func: Callable, img_path,
    ) -> None:
        represent_image_on_path = partial(func, img_path=img_path)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor,
            represent_image_on_path,
        )
