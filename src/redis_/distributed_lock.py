import datetime
import functools
import threading
import time

import redis

# Подключение к redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def single(max_processing_time: datetime.timedelta):
    """
    Декоратор, который гарантирует, что функция не выполняется параллельно.
    При параллельном вызове функции, она будет ожидать, пока текущая инстанция функции завершит свою работу.

    Метод lock.release использует Lua-скрипт внутри, который атомарно проверяет и удаляет ключ блокировки.
    Это гарантирует, что только тот клиент, который захватил блокировку, может её освободить.

    :param max_processing_time: Максимальное время выполнения функции.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Создание уникального идентификатора блокировки и ключа для блокировки
            lock_name = f"lock:{func.__name__}"
            lock = redis_client.lock(
                lock_name, timeout=int(max_processing_time.total_seconds())
            )

            # Проверка блокировки
            if not lock.acquire(blocking=False):
                raise Exception("Функция уже выполняется или занята другим процессом")

            try:
                return func(*args, **kwargs)
            finally:
                # Освобождение блокировки
                lock.release()

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction(thread_id: int) -> None:
    """
    Имитация транзакции.

    :param thread_id: Идентификатор потока.
    """

    print(f"Поток {thread_id}: Начало выполнения транзакции...")
    time.sleep(2)
    print(f"Поток {thread_id}: Транзакция завершена.")


def run_transaction(thread_id: int) -> None:
    """
    Запуск транзакции в отдельном потоке.

    :param thread_id: Идентификатор потока.
    """

    try:
        process_transaction(thread_id)
    except Exception as e:
        print(f"Поток {thread_id}: Ошибка - {e}")


if __name__ == "__main__":
    # Создание двух потоков
    thread1 = threading.Thread(target=run_transaction, args=(1,))
    thread2 = threading.Thread(target=run_transaction, args=(2,))

    # Запуск потоков
    thread1.start()
    time.sleep(0.1)  # Задержка, чтобы первый поток успел захватить блокировку
    thread2.start()

    # Ожидание завершения потоков
    thread1.join()
    thread2.join()
