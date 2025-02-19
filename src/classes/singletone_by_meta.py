"""
Реализовать паттерн синглтон тремя способами:

1. с помощью метаклассов
2. с помощью метода __new__ класса
3. через механизм импортов
"""


# Реализация синглтона с помощью метакласса
class SingletoneMeta(type):
    """
    Метакласс для создания одного экземпляра класса.
    """

    # словарь объектов
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        При вызове класса создает или возвращает уже созданный экземпляр.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletoneClass(metaclass=SingletoneMeta):
    """
    Класс синглтона.
    """

    def __init__(self, name):
        self.name = name


bob = SingletoneClass("Bob")
alice = SingletoneClass("Alice")

print(bob is alice)  # Output: True - это один и тот же экземпляр
print(bob.name)  # Output: Bob
print(alice.name)  # Output: Bob
