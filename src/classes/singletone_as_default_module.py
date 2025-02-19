"""
Реализовать паттерн синглтон тремя способами:

1. с помощью метаклассов
2. с помощью метода __new__ класса
3. через механизм импортов
"""


class SingletoneClass:
    """
    Класс синглтона.
    """

    def __init__(self, name):
        self.name = name


person = SingletoneClass("Bob")
