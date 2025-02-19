import random


def generate_data(number: int) -> list[int]:
    """
    Генерирует случайные числа в диапазоне от 1 до 1000

    :param number: Количество случайных целых чисел
    :return: Список случайных целых чисел
    """

    return [random.randint(1, 1000) for i in range(number)]
