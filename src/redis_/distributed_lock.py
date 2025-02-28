import datetime
import functools
import threading
import time
import uuid

import redis

# Подключение к redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def single(max_processing_time: datetime.timedelta):
    """
    Декоратор, который гарантирует, что функция не выполняется параллельно.
    При параллельном вызове функции, она будет ожидать, пока текущая инстанция функции завершит свою работу.

    :param max_processing_time: Максимальное время выполнения функции.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Создание уникального идентификатора блокировки и ключа для блокировки
            lock_id = str(uuid.uuid4())
            lock_key = f"lock:{func.__name__}"

            # Проверка наличия блокировки
            acquired = redis_client.set(
                lock_key, lock_id, nx=True, ex=int(max_processing_time.total_seconds())
            )

            if not acquired:
                raise Exception("Функция уже выполняется или занята другим процессом")

            try:
                return func(*args, **kwargs)
            finally:
                # Освобождение блокировки
                if redis_client.get(lock_key) == lock_id.encode():
                    redis_client.delete(lock_key)

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
