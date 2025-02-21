"""
Напишите асинхронную функцию fetch_urls, которая принимает файл со списком урлов (каждый URL адрес возвращает JSON)
и сохраняет результаты выполнения в другой файл (result.jsonl), где ключами являются URL,
а значениями — распарсенный json, при условии, что статус код — 200. Используйте библиотеку aiohttp
для выполнения HTTP-запросов.

Требования:
- Ограничьте количество одновременных запросов до 5.
- Обработайте возможные исключения (например, таймауты, недоступные ресурсы) ошибок соединения.

Контекст:
- Урлов в файле может быть десятки тысяч.
- Некоторые урлы могут весить до 300-500 мегабайт.
- При внезапной остановке и/или перезапуске скрипта - допустимо скачивание урлов по новой.
"""

import asyncio
import json
import logging
from typing import Any

import aiofiles
import aiohttp
from aiohttp import ClientSession, ClientTimeout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("errors.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


async def process_url(
    session: ClientSession, queue: asyncio.Queue, out_file: Any
) -> None:
    """
    Асинхронно обрабатывает один URL, выполняя HTTP-запрос и записывая полученный JSON-ответ в файл в формате JSONL.

    :param session: Объект `aiohttp.ClientSession` для HTTP-запросов.
    :param queue: Очередь (`asyncio.Queue`), из которой извлекаются URL для обработки.
    :param out_file: Асинхронный файловый объект для записи результатов в формате JSONL.
    """

    try:
        while True:
            url = await queue.get()

            try:
                async with session.get(
                    url, timeout=ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        content_type = response.headers.get("Content-Type", "")

                        if "json" not in content_type.lower():
                            logging.warning(
                                f"Контент типа JSON отсутствует на {url}. Пропуск..."
                            )
                            continue
                        try:
                            content = await response.json(content_type=None)
                            await out_file.write(
                                json.dumps({url: content}, ensure_ascii=False) + "\n"
                            )
                        except (aiohttp.ContentTypeError, json.JSONDecodeError) as e:
                            logging.error(
                                f"Ошибка парсинга JSON на {url}: {e}. Пропуск..."
                            )
                    else:
                        logging.warning(
                            f"Получен статус-код {response.status} для URL: {url}. Пропуск..."
                        )
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logging.error(f"Ошибка соединения: {url}: {e}. Пропуск...")
            finally:
                queue.task_done()
    except asyncio.CancelledError:
        logging.info("Worker завершил работу")


async def url_producer(input_file: str, queue: asyncio.Queue):
    """
    Считывает url из файла построчно и помещает их в очередь.

    :param input_file: Путь к текстовому файлу со списком URL-адресов (один URL на строку).
    :param queue: Очередь для хранения URL-адресов.
    """

    async with aiofiles.open(input_file, "r") as file:
        async for line in file:
            url = line.strip()

            if url and url.startswith(("http://", "https://")):
                await queue.put(url)


async def fetch_urls(
    input_file: str, output_file: str, max_concurrent: int = 5
) -> None:
    """
    Асинхронная функция для загрузки списка URL-адресов и сохранения результатов в формате JSONL.

    :param input_file: Путь к текстовому файлу со списком URL-адресов (один URL на строку).
    :param output_file: Путь к файлу для записи результатов (каждая строка в формате JSONL).
    :param max_concurrent: Количество одновременных запросов
    """

    queue = asyncio.Queue(maxsize=1000)
    timeout = 60

    async with (
        aiohttp.ClientSession() as session,
        aiofiles.open(output_file, "w") as out_file,
    ):
        producer_task = asyncio.create_task(url_producer(input_file, queue))

        workers = [
            asyncio.create_task(process_url(session, queue, out_file))
            for i in range(max_concurrent)
        ]

        try:
            await producer_task
        except Exception as e:
            logging.error(f"Ошибка в producer: {e}")
            raise
        finally:
            try:
                await asyncio.wait_for(queue.join(), timeout=timeout)
            except asyncio.TimeoutError:
                logging.warning(
                    "Время ожидания завершения обработки очереди истекло. Таймаут: {timeout} сек."
                )

            for worker in workers:
                worker.cancel()
            await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "./results2.jsonl"))
