## Что такое рекурсия? Приведите пример рекурсивной функции.
> **Ответ:**
>
> `Рекурсия` — это когда функция вызывает саму себя для решения задачи. 
> Она состоит из двух частей: базовый случай (когда рекурсия останавливается) и рекурсивный случай (когда функция вызывает себя).

**Пример:**
Функция вычисляет факториал числа `n`
```python
def factorial(n):
    if n == 1:  # базовый случай
        return 1
    else:  # рекурсивный случай
        return n * factorial(n - 1)
```

> Для рекурсии всегда должно быть условие, которое определяет базовый случай. Без базового случая рекурсия будет продолжаться бесконечно, что приведет к переполнению стека вызовов и ошибке (RecursionError).

### Почему базовый случай важен?
`Базовый случай `— это условие, при котором рекурсия останавливается. 
Оно предотвращает бесконечный вызов функции самой себя.

`Рекурсивный случай` — это часть функции, где она вызывает саму себя, двигаясь к базовому случаю.

### Итог:
`Базовый случай` обязателен для рекурсии, чтобы она могла завершиться.
Без базового случая рекурсия будет продолжаться бесконечно, что приведет к ошибке.


## Как декораторы работают с асинхронными функциями
Декораторы могут работать с асинхронными функциями, но нужно учитывать особенности асинхронного кода. 
Асинхронные функции возвращают корутины (`coroutine`), которые должны быть приостановлены `await`, 
поэтому декораторы для асинхронных функций должны быть написаны с учетом этого.

1. Базовый пример декоратора для асинхронной функции
> Декоратор для асинхронной функции должен быть асинхронным сам или возвращать асинхронную функцию-обертку.


```python
import asyncio

def async_decorator(func):
    async def wrapper(*args, **kwargs):
        print("До вызова функции")
        result = await func(*args, **kwargs)  # await, так как func — асинхронная
        print("После вызова функции")
        return result
    return wrapper

@async_decorator
async def my_async_function():
    print("Асинхронная функция выполняется")
    await asyncio.sleep(1)
    return "Готово!"

async def main():
    result = await my_async_function()
    print(result)

asyncio.run(main())
```
**Результат:**

```text
До вызова функции
Асинхронная функция выполняется
После вызова функции
Готово!
```
2. Декоратор с аргументами для асинхронных функций
> Декоратор с аргументами для асинхронных функций работает так же, как и для синхронных, но нужно учитывать асинхронную природу.

```python
import asyncio

def repeat(num_times):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
async def my_async_function():
    print("Асинхронная функция выполняется")
    await asyncio.sleep(1)
    return "Готово!"

async def main():
    result = await my_async_function()
    print(result)

asyncio.run(main())
```

**Результат:**

```text
Асинхронная функция выполняется
Асинхронная функция выполняется
Асинхронная функция выполняется
Готово!
```

3. Декоратор, который работает и с синхронными, и с асинхронными функциями
> Иногда нужно создать универсальный декоратор, который может работать как с синхронными, так и с асинхронными функциями. 
> Для этого можно использовать inspect.iscoroutinefunction, чтобы проверить, является ли функция асинхронной.

```python
import asyncio
import inspect

def universal_decorator(func):
    if inspect.iscoroutinefunction(func):
        async def async_wrapper(*args, **kwargs):
            print("Асинхронная функция запущена")
            result = await func(*args, **kwargs)
            print("Асинхронная функция завершена")
            return result
        return async_wrapper
    else:
        def sync_wrapper(*args, **kwargs):
            print("Синхронная функция запущена")
            result = func(*args, **kwargs)
            print("Синхронная функция завершена")
            return result
        return sync_wrapper

@universal_decorator
async def my_async_function():
    print("Асинхронная функция выполняется")
    await asyncio.sleep(1)
    return "Готово!"

@universal_decorator
def my_sync_function():
    print("Синхронная функция выполняется")
    return "Готово!"

async def main():
    print(await my_async_function())
    print(my_sync_function())

asyncio.run(main())
```

**Результат:**

```text
Асинхронная функция запущена
Асинхронная функция выполняется
Асинхронная функция завершена
Готово!
Синхронная функция запущена
Синхронная функция выполняется
Синхронная функция завершена
Готово!
```

4. Декораторы для асинхронных методов класса
> Декораторы также могут применяться к асинхронным методам класса. 
> Принцип работы тот же, что и для обычных асинхронных функций.

```python
import asyncio

def async_decorator(func):
    async def wrapper(*args, **kwargs):
        print("Декоратор: до вызова метода")
        result = await func(*args, **kwargs)
        print("Декоратор: после вызова метода")
        return result
    return wrapper

class MyClass:
    @async_decorator
    async def my_async_method(self):
        print("Метод выполняется")
        await asyncio.sleep(1)
        return "Готово!"

async def main():
    obj = MyClass()
    result = await obj.my_async_method()
    print(result)

asyncio.run(main())
```
**Результат:**

```text
import asyncio

def async_decorator(func):
    async def wrapper(*args, **kwargs):
        print("Декоратор: до вызова метода")
        result = await func(*args, **kwargs)
        print("Декоратор: после вызова метода")
        return result
    return wrapper

class MyClass:
    @async_decorator
    async def my_async_method(self):
        print("Метод выполняется")
        await asyncio.sleep(1)
        return "Готово!"

async def main():
    obj = MyClass()
    result = await obj.my_async_method()
    print(result)

asyncio.run(main())
```

5. Проблемы и подводные камни
- **Ошибка с `await`:** Если забыть добавить `await` внутри декоратора для асинхронной функции, 
это приведет к ошибке или некорректному поведению.
- **Сложность отладки:** Асинхронные декораторы могут усложнить отладку, особенно если они вложенные.
- **Производительность:** Добавление декораторов к асинхронным функциям может немного увеличить накладные расходы.

### Итог:
- Декораторы для асинхронных функций должны быть асинхронными или возвращать асинхронную функцию-обертку.
- Обязательно использование `await` для вызова асинхронной функции внутри декоратора.
- Декораторы могут быть универсальными и работать как с синхронными, так и с асинхронными функциями.
- Осторожнее с ошибками и накладными расходами при использовании декораторов с асинхронным кодом.
