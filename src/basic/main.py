# Неизменяемые типы - immutable types

int
a = 10
print(id(a))  # Допустим, выводит: 140711223676608
a += 5  # Создает новый объект со значением 15
print(id(a))  # Выводит другой идентификатор, например: 140711223676688

# str
s = "Hello"
# Попытка изменить символ строки приведет к ошибке
# s[0] = "h"  # TypeError: 'str' object does not support item assignment
print(f"Hash if 'string': {hash(s)}")  # Выведет какое-то число, например, 123456789

n = 42
print(f"Hash if 'int': {hash(n)}")  # Выведет 42, потому что хэш числа — это само число

t = (1, 2, 3)
print(f"Hash if 'tuple': {hash(t)}")  # Выведет какое-то число

print(f"{True + True = }, {True + False = }, {False + False = }")
print(f"{True is True = }, {True is False = }, {False is False = }")

# Изменяемые типы - mutable types
empty_list = []
print(
    f"{empty_list is True = }, {empty_list is False = }"
)  # empty_list is True = False, empty_list is False = False
print(bool(empty_list))  # False
# Оператор is работает только с объектами True и False, а не с их логической интерпретацией.

# Пример нехэшируемости:
# Списки не хэшируемы, потому что они изменяемы (их можно изменить после создания).
# Словари тоже не хэшируемы, потому что они изменяемы.


# Зачем нужна хэшируемость?
# Хэшируемость позволяет эффективно использовать объекты в структурах данных, которые полагаются на хэши, например:


# Пример с хэш-коллизией:
# Иногда разные объекты могут иметь одинаковый хэш (это называется коллизией). Python обрабатывает такие случаи:
a = "hello"
b = "HELLO"
print(hash(a) == hash(b))  # Маловероятно, но возможно

# Пример передачи переменной в качестве значения по умолчанию
good_number = 10


def get_number(number=good_number):
    return number


print(get_number())  # Выведет 10

good_number = 20  # Изменяем переменную
print(get_number())  # Всё равно выведет 10 — значение по умолчанию "зафиксировано"

# Пример match...case
day = "tuesday"

match day:
    case "monday":
        print("It's Monday!")
    case "tuesday":
        print("It's Tuesday!")
    case "wednesday":
        print("It's Wednesday!")
    case "thursday":
        print("It's Thursday!")
    case "friday":
        print("It's Friday!")
    case "saturday":
        print("It's Saturday!")
    case "sunday":
        print("It's Sunday!")
    case _:
        print("Unknown day!")

# Пример опустошения списка через цикл
simple_line = "spam foo bar eggs"
words_array = simple_line.split()

while words_array:
    word = words_array.pop()
    print(f"{word = }")
    print(f"{words_array = }")
