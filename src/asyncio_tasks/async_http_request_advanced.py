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

from aiohttp import ClientSession
from asyncio import Semaphore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("errors.log"), logging.StreamHandler()],
)


async def process_url(url: str, session: ClientSession, semaphore: Semaphore, out_file: Any) -> None:
    """
    Асинхронно обрабатывает один URL, выполняя HTTP-запрос и записывая полученный JSON-ответ в файл в формате JSONL.

    :param url: URL-адрес для выполнения запроса.
    :param session: Объект `aiohttp.ClientSession` для осуществления HTTP-запросов.
    :param semaphore: Объект `asyncio.Semaphore`, ограничивающий количество одновременных запросов.
    :param out_file: Асинхронный файловый объект для записи результатов в формате JSONL.
    """

    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=10)

            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")

                    # Проверяем, что ответ действительно JSON
                    if "application/json" not in content_type:
                        logging.warning(f"Non-JSON response from {url}")
                        return

                    try:
                        content = await response.json()
                        data = {"url": url, "content": content}
                        line = json.dumps(data, ensure_ascii=False) + "\n"
                        await out_file.write(line)
                    except (aiohttp.ContentTypeError, json.JSONDecodeError) as e:
                        logging.error(f"JSON parse error: {url} | {str(e)}")
                else:
                    logging.warning(f"Status {response.status} for {url}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"Connection error: {url} | {str(e)}")


async def fetch_urls(input_file: str, output_file: str) -> None:
    """
    Асинхронная функция для загрузки списка URL-адресов и сохранения результатов в формате JSONL.

    :param input_file: Путь к текстовому файлу со списком URL-адресов (один URL на строку).
    :param output_file: Путь к файлу для записи результатов (каждая строка в формате JSONL).
    """

    with open(input_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(output_file, "w") as out_file:
            tasks = []

            for url in urls:
                task = asyncio.create_task(
                    process_url(url, session, semaphore, out_file)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "./results2.jsonl"))
