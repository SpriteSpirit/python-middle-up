"""
Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и возвращает словарь,
где ключами являются URL, а значениями — статус-коды ответов.
Используйте библиотеку aiohttp для выполнения HTTP-запросов.
"""

import aiohttp
import asyncio
import json


async def fetch_urls(urls: list[str], file_path: str):
    """
    Асинхронно отправляет HTTP-запросы к списку URL-адресов и сохраняет их статус-коды в JSON-файл.

    :param urls: Список URL-адресов для запроса.
    :param file_path: Путь к JSON-файлу, где будет сохранен результат.
    """

    async with aiohttp.ClientSession() as session:
        # Ограничение кол-ва одновременных запросов
        semaphore = asyncio.Semaphore(5)
        tasks = []

        async def fetch(url: str):
            """
            Выполняет HTTP-запрос GET к указанному URL и возвращает кортеж (URL, статус-код).

            :param url: URL-адрес для запроса.
            :return: Кортеж (URL, статус-код)
            """

            async with semaphore:
                try:
                    async with session.get(url, timeout=10) as response:
                        return url, response.status
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    # Где 0 - ошибка запроса
                    return url, 0

        # Создание задач для всех URL
        tasks = [fetch(url) for url in urls]
        # Ожидание выполнения всех задач
        results = await asyncio.gather(*tasks)

        # Сохранение результатов в JSON-файл
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([{"url": url, "status_code": status_code} for url, status_code in results], file, indent=4)


if __name__ == '__main__':
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url"
    ]
    asyncio.run(fetch_urls(urls, './results.json'))
