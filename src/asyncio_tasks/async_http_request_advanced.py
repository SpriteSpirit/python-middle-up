import asyncio
import json
import logging
import typing

import aiofiles
import aiohttp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("errors.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


async def process_url(
    session: aiohttp.ClientSession, url: str
) -> typing.Optional[dict]:
    """
    Обрабатывает URL, выполняет запрос и парсит JSON-ответ.

    :param session: Объект aiohttp.ClientSession для выполнения HTTP-запросов.
    :param url: URL-адрес для обработки.
    """

    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
        if response.status != 200:
            logging.warning(
                f"Получен статус-код {response.status} для URL: {url}. Пропуск..."
            )
            return None

        content_type = response.headers.get("Content-Type", "")

        if "json" not in content_type.lower():
            logging.warning(f"Контент типа JSON отсутствует на {url}. Пропуск...")
            return None

        try:
            return await response.json()
        except (aiohttp.ContentTypeError, json.JSONDecodeError) as e:
            logging.error(f"Ошибка парсинга JSON на {url}: {e}. Пропуск...")
            return None


async def worker(
    session: aiohttp.ClientSession, queue_in: asyncio.Queue, queue_out: asyncio.Queue
) -> None:
    """
    Рабочая задача, обрабатывающая URL из входной очереди.

    :param session: Объект aiohttp.ClientSession для выполнения HTTP-запросов.
    :param queue_in: Очередь входных URL для обработки.
    :param queue_out: Очередь для хранения результатов обработки.
    """

    while True:
        url = await queue_in.get()

        if url is None:
            queue_in.task_done()
            return

        try:
            result = await process_url(session, url)
            if result is not None:
                await queue_out.put({url: result})  # Добавлено URL как ключ
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"Ошибка обработки URL: {url}, {e}")
        finally:
            queue_in.task_done()


async def writer(file, queue: asyncio.Queue) -> None:
    """
    Записывает результаты в JSON-файл.

    :param file: Объект aiofiles для записи результатов.
    :param queue: Очередь для хранения результатов обработки.
    """

    while True:
        data = await queue.get()

        if data is None:
            queue.task_done()
            return

        await file.write(json.dumps(data) + "\n")  # Запись результата в формате JSON


async def url_producer(input_file: str, queue: asyncio.Queue) -> None:
    """
    Считывает URL из входного файла и помещает их в очередь.

    :param input_file: Имя файла с входными URL.
    :param queue: Очередь для хранения входных URL.
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
    Запускает процесс асинхронной загрузки URL и записи результатов в файл.

    :param input_file: Имя файла с входными URL.
    :param output_file: Имя файла для записи результатов.
    :param max_concurrent: Максимальное количество одновременных запросов.
    """

    queue_in = asyncio.Queue(maxsize=1000)
    queue_out = asyncio.Queue(maxsize=1000)

    async with (
        aiohttp.ClientSession() as session,
        aiofiles.open(output_file, "w") as out_file,
    ):
        # Запуск worker-потоков и writer-потока
        workers = [
            asyncio.create_task(worker(session, queue_in, queue_out))
            for _ in range(max_concurrent)
        ]
        writer_task = asyncio.create_task(writer(out_file, queue_out))

        # Запускает корутину и ждет ее завершения
        await url_producer(input_file, queue_in)

        for _ in range(max_concurrent):
            # Уведомление workers о завершении
            await queue_in.put(None)

        # Ожидание завершения всех workers
        await queue_in.join()
        # Уведомление writer о завершении
        await queue_out.put(None)
        # Ожидание завершения writer-потока
        await writer_task
        # Проверка, что все workers завершены
        await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "./results2.jsonl"))
