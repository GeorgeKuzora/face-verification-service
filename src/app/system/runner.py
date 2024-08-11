import asyncio
from concurrent.futures import Executor, ProcessPoolExecutor
from typing import Any, Callable


class AsyncMultiProccessRunner:
    """Раннер для запуска а асинхронной функции в новом процессе."""

    async def run(self, func: Callable, **kwargs) -> Any:
        """
        Метод запуска функции.

        :param func: Запускаемая функция
        :type func: Callable
        :param kwargs: Атрибуты функциив форме ключ-значение
        :type kwargs: key-value pairs
        """
        with ProcessPoolExecutor() as pool:
            asyncio.run(
                self._run(pool, func, **kwargs),
            )

    async def _run(
        self, executor: Executor, func: Callable, **kwargs,
    ) -> None:
        loop = asyncio.get_event_loop()
        await asyncio.gather(
            loop.run_in_executor(
                executor,
                lambda: func(**kwargs),
            ),
        )

class SimpleAsyncRunner:

    async def run(self, func: Callable, **kwargs) -> Any:
        """
        Метод запуска функции.

        :param func: Запускаемая функция
        :type func: Callable
        :param kwargs: Атрибуты функциив форме ключ-значение
        :type kwargs: key-value pairs
        """
        await func(**kwargs)
