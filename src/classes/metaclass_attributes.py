"""
Написать мета класс, который автоматически добавляет атрибут created_at с текущей датой и временем
к любому классу, который его использует.
"""

import datetime


class MetaClassCreatedAt(type):
    """
    Метакласс для автоматического добавления атрибута created_at с текущей датой и временем к любому классу.
    """

    def __new__(cls, name, bases, namespace):
        """
        Переопределяем метод __new__ для добавления атрибута created_at с текущей датой и временем.
        :param cls: Класс, который будет использовать данный метакласс.
        :param name: Имя нового класса.
        :param bases: Базовые классы нового класса.
        :param namespace: Словарь атрибутов и методов нового класса.
        :return: Новый экземпляр класса.
        """

        namespace["created_at"] = datetime.datetime.now()
        return type.__new__(cls, name, bases, namespace)


class MetaClassAttributes(metaclass=MetaClassCreatedAt):
    """
    Класс с автоматическим добавлением атрибута created_at с текущей датой и временем.
    """

    pass


# Выводит текущее время создания класса
print(MetaClassAttributes.created_at)
