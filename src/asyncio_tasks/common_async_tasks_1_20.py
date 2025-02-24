# --------------- Задачи 1-20 --------------- #
import asyncio
import time

import aiofiles


# 1. Простая асинхронная функция.
async def print_message(msg: str) -> None:
    """
    Асинхронная функция, которая выводит сообщение через 1 секунду.
    """

    await asyncio.sleep(1)
    print(msg)


# 2. Запуск двух корутин подряд.
async def print_msg1(msg: str) -> None:
    """
    Корутина для печати сообщения.
    """

    await asyncio.sleep(1)
    print(msg)


async def print_msg2(msg: str) -> None:
    """
    Корутина для печати сообщения.
    """

    await asyncio.sleep(1)
    print(msg)


# 3. Параллельный запуск двух корутин
async def print_msg_in_row():
    """
    Основная функция, которая запускает две корутины и ждет завершения их выполнения.
    """

    await print_msg1("Hello")
    await print_msg2("World!")


async def print_msg_parallel():
    """
    Основная функция, которая запускает две корутины параллельно и ждет завершения их выполнения.
    """

    await asyncio.gather(print_msg1("Hello"), print_msg2("World!"))


# 4. Передача аргументов в корутину
async def greeting(*names: tuple) -> None:
    """
    Асинхронная функция, которая выводит приветствие каждому из имен.
    """

    for name in names:
        await asyncio.sleep(1)
        print(f"Hello, {name}!")


# 5. Повторение действия с задержкой
async def repeat(times: int) -> None:
    """
    Асинхронная функция, которая повторяет сообщение заданное число раз.
    """

    for _ in range(times):
        await asyncio.sleep(1)
        print("Tick")


# 6. Измерение времени выполнения
async def wait_for_seconds(seconds: int) -> None:
    """
    Асинхронная функция, которая делает задержку на указанное число секунд.
    """
    await asyncio.sleep(seconds)
    print(f"Прошло {seconds} с.")


async def measure_time() -> None:
    """
    Асинхронная функция, которая измеряет время выполнения кода.
    """
    start_time = time.time()
    await asyncio.gather(wait_for_seconds(2), wait_for_seconds(2))
    end_time = time.time()
    print(f"Время исполнения: {round(end_time - start_time, 2)} с.")


# 7. Асинхронное ожидание с timeout
async def long_time_task(seconds: int) -> None:
    """
    Асинхронная функция, которая выполняет долгую задачу.
    """
    await asyncio.sleep(seconds)
    print(f"Продолжительная задача длиной {seconds} с.")


async def timeout_task(timeout: int) -> None:
    """
    Асинхронная функция, которая выполняет долгую задачу с таймаутом.
    """

    try:
        await asyncio.wait_for(long_time_task(3), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Время выполнения задачи превысило {timeout} с.")


# 8. Простая очередь с задачами
async def worker(queue: asyncio.Queue) -> None:
    while True:
        msg = await queue.get()

        if msg is None:  # Сигнал завершения
            queue.task_done()
            break
        print(msg)
        queue.task_done()


async def print_msg_with_queue(max_workers: int) -> None:
    queue = asyncio.Queue()
    await queue.put("Hello")
    await queue.put("world!")
    workers = [asyncio.create_task(worker(queue)) for _ in range(max_workers)]

    for _ in range(max_workers):
        await queue.put(None)

    await asyncio.gather(*workers)
    await queue.join()


# 9. Создание задачи вручную
async def print_some_msg(msg: str) -> None:
    await asyncio.sleep(1)
    print(msg)


async def manual_create_task() -> None:
    """
    asyncio.create_task создает объект Task из корутины print_some_msg("Hello!") и немедленно запускает её выполнение в фоновом режиме (в цикле событий).
    await task ожидает завершения этой задачи.
    Задача начинает выполняться сразу после создания, даже до await.
    Это позволяет запускать задачу параллельно с другими операциями в рамках одной функции.
    Например, можно создать несколько задач и управлять их выполнением (ждать, отменять и т.д.).
    Если вы хотите запустить задачу в фоне и, возможно, продолжить выполнение другого кода в той же функции перед её завершением.
    Полезно для параллельного выполнения нескольких задач.
    """

    task = asyncio.create_task(print_some_msg("Hello!"))
    await task


# 10. Отмена задачи
async def worker() -> None:
    print("Worker запустился")
    await asyncio.sleep(5)
    print("Worker отработал")


async def canceled_task() -> None:
    task = asyncio.create_task(worker())
    await asyncio.sleep(1)
    task.cancel()
    print("Задача отменена")

    # Подтверждение завершения задачи
    try:
        await task
    except asyncio.CancelledError:
        print("Задача была отменена")


# 11. Параллельная обработка списка
async def process_number(number: float) -> None:
    await asyncio.sleep(1)
    print(f"Число: {number}")


async def print_numbers() -> None:
    numbers = [1, 2, 3, 4, 5]

    tasks = [process_number(number) for number in numbers]
    await asyncio.gather(*tasks)


# 12. Ограничение параллельных задач
async def some_task(active_task: int, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        await asyncio.sleep(1)
        print(f"Задача {active_task} завершена")


async def limited_task(limit: int = 5) -> None:
    semaphore = asyncio.Semaphore(limit)
    tasks = [some_task(i, semaphore) for i in range(limit)]

    await asyncio.gather(*tasks)


# 13. Обработка исключений
async def throw_exception() -> None:
    await asyncio.sleep(1)
    raise ValueError("Что-то пошло не так")


async def handle_exception() -> None:
    try:
        await throw_exception()
        print("Задача завершена без ошибок")
    except ValueError as e:
        print(f"Произошла ошибка: {e}")


# 14. Очередь с несколькими воркерами
async def worker(queue: asyncio.Queue) -> None:
    while not queue.empty():
        number = await queue.get()
        await asyncio.sleep(1)
        print(f"Worker обработал число: {number}")
        queue.task_done()


async def process_number(count_number: int = 3) -> None:
    queue = asyncio.Queue()

    for i in range(count_number):
        await queue.put(i)

    await asyncio.gather(worker(queue), worker(queue))
    await queue.join()


# 15. Асинхронное чтение файла
async def process_file(file_path: str) -> None:
    async with aiofiles.open("async_test.txt", "r", encoding="utf-8") as file:
        async for line in file:
            await asyncio.sleep(0.5)
            print(line.strip())


# 16. Параллельные запросы с задержкой
async def fake_requests(delay: int) -> None:
    await asyncio.sleep(delay)
    print(f"Запрос после {delay} секунд")


async def process_requests() -> None:
    await asyncio.gather(fake_requests(1), fake_requests(2), fake_requests(3))


# 17. Ожидание первой завершившейся задачи
async def some_task(delay: int) -> str:
    await asyncio.sleep(delay)
    return f"Задача с задержкой {delay} с."


async def wait_first_completed_task(task_count: int = 3) -> None:
    tasks = [asyncio.create_task(some_task(i)) for i in range(1, task_count + 1)]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        print(task.result())

    for task in pending:
        task.cancel()


# 18. Последовательная обработка с условием
async def even_numbers(numbers: list) -> None:
    for number in numbers:
        if number % 2 == 0:
            await asyncio.sleep(1)
            print(number)


# 19. Семафор с обработкой ошибок
async def new_task(
    task_number: int, semaphore: asyncio.Semaphore, task_count: int
) -> None:
    async with semaphore:
        await asyncio.sleep(1)

        exception_task = 2

        if exception_task == task_number:
            raise ValueError(f"Ошибка в задаче {task_number} ")
        print(f"Задача {task_number} успешно завершена")


async def semaphore_with_exception(task_count: int) -> None:
    semaphore = asyncio.Semaphore(2)
    tasks = [new_task(i, semaphore, 5) for i in range(task_count)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            print(f"Произошла ошибка: {result}")

# 20. Асинхронный генератор
async def async_generator() -> int:
    for i in range(1, 4):
        await asyncio.sleep(1)
        yield i

async def print_gen() -> None:
    async for i in async_generator():
        print(f'Число: {i}')


if __name__ == "__main__":
    # asyncio.run(print_message('Hello, asyncio!'))
    # asyncio.run(print_msg_in_row())
    # asyncio.run(print_msg_parallel())
    # asyncio.run(greeting('Alice', 'Bob', 'Charlie'))
    # asyncio.run(repeat(3))
    # asyncio.run(measure_time())
    # asyncio.run(timeout_task(1))
    # asyncio.run(print_msg_with_queue(12))
    # asyncio.run(manual_create_task())
    # asyncio.run(print_some_msg('Hello!'))
    # asyncio.run(canceled_task())
    # asyncio.run(print_numbers())
    # asyncio.run(limited_task())
    # asyncio.run(handle_exception())
    # asyncio.run(process_number())
    # asyncio.run(process_file('async_test.txt'))
    # asyncio.run(process_requests())
    # asyncio.run(wait_first_completed_task())
    # asyncio.run(even_numbers([1, 2]))
    # asyncio.run(even_numbers([1, 2]))
    # asyncio.run(semaphore_with_exception(5))
    asyncio.run(print_gen())
