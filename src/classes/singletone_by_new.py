"""
Реализовать паттерн синглтон тремя способами:

1. с помощью метаклассов
2. с помощью метода __new__ класса
3. через механизм импортов
"""


class SingletoneClass():
    """
    Класс синглтона.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.name = name


bob = SingletoneClass("Bob")
alice = SingletoneClass("Alice")
tedd = SingletoneClass("Tedd")

print(bob is alice)  # Output: True - это один и тот же экземпляр
print(bob.name)  # Output: Alice (значение изменилось, так как это тот же экземпляр и объект Alice был создан последним)
print(alice.name)  # Output: Alice
