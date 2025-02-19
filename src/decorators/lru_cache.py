import unittest.mock
from collections import OrderedDict
from functools import wraps


def lru_cache(maxsize=None):
    """
    Декоратор для кэширования результатов функции с использованием LRU (Least Recently Used),
    который удаляет давно неиспользуемые элементы при заполнении кеша.

    :param maxsize: Максимальное число элементов в кэше. Если не указано, кэш не ограничен.
    :return: Декоратор
    """

    def decorator(func):
        """
        Принимает функцию, которая будет обернута кешированием.
        Создает упорядоченный словарь cache для хранения кэша.
        OrderedDict сохраняет порядок добавления элементов для реализации LRU
        :param func: Другая функция
        :return: Обертка
        """
        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Декоратор-обертка для сохранения метаданных исходной функции.
            Вызывается вместо func с сохраненными аргументами и сохраняет результат в кэше.
            :param args: Любое кол-во позиционных аргументов
            :param kwargs: Любое кол-во именованных аргументов
            :return: Результат сохраняется в кэше
            """
            # Создание уникального ключа для кэша на основе аргументов функции
            key = (args, tuple(sorted(kwargs.items())))

            # Если результат уже в кэше, возвращает его
            if key in cache:
                # Перемещение ключа в конец, чтобы отметить его как недавно использованный
                cache.move_to_end(key)

                # Возвращение закэшированного результата
                return cache[key]

            # Если кэш заполнен, удаляется самый старый элемент из кэша
            if maxsize is not None and len(cache) >= maxsize:
                # last=False - элемент удаляется з начала упорядоченного словаря, кот. является самым старым
                cache.popitem(last=False)

            # Вызов функции и сохранение результата в кэше
            result = func(*args, **kwargs)
            cache[key] = result

            return result

        return wrapper

    # Если декоратор вызван без аргументов, возвращаем сам декоратор
    # В этом случае maxsize будет содержать саму функцию, которую нужно обернуть
    if callable(maxsize):
        func = maxsize
        maxsize = None
        return decorator(func)
    else:
        return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
