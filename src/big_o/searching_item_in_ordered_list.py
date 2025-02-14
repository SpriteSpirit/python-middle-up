sorted_list = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def search(number: id) -> bool:
    """
    Функция поиска числа в отсортированном списке.

    :param number: Искомое число
    :return: True, если число найдено в списке, False - если нет
    """

    left, right = 0, len(sorted_list) - 1

    while left <= right:
        middle = (left + right) // 2
        print(middle)

        if not sorted_list:
            return False

        if sorted_list[middle] == number:
            return True
        elif sorted_list[middle] < number:
            left = middle + 1
        else:
            right = middle - 1

    return False

# Пример использования
# print(search(356))  # Output: True
# print(search(1000))  # Output: False
# print(search(923))  # Output: True
# print(search(755))  # Output: False
# print(search(2))  # Output: True
# print(search(45))  # Output: True
