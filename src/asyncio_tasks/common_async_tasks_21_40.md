### Простые задачи

21. **Асинхронный input()**

**Задача:** Напишите асинхронную функцию, которая ждет ввода пользователя и выводит этот ввод с задержкой 1 секунда.
<details>       
<summary><b>Решение</b></summary> <br>

   ```python
import asyncio

async def async_input(prompt):
   print(prompt, end='', flush=True)
   loop = asyncio.get_running_loop()
   result = await loop.run_in_executor(None, input)
   await asyncio.sleep(1)
   return result

async def main():
   user_input = await async_input("Enter something: ")
   print(f"You entered: {user_input}")

asyncio.run(main())
```
</details>

22. **Асинхронный счетчик**

**Задача:** Создайте асинхронный счетчик, который увеличивает значение каждую секунду и выводит его в консоль.

<details>       
<summary><b>Решение</b></summary> <br>

```python
    import asyncio
    
    async def counter(max_count):
       for i in range(1, max_count + 1):
           await asyncio.sleep(1)
           print(i)
    
    async def main():
       await counter(5)
    
    asyncio.run(main())
```
</details>

23. **Асинхронное чтение и запись в файл**

**Задача:** Асинхронно прочитайте строки из файла `input.txt` и асинхронно запишите их в файл `output.txt`.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import aiofiles

   async def copy_file(input_file, output_file):
       async with aiofiles.open(input_file, mode='r') as in_f:
           async with aiofiles.open(output_file, mode='w') as out_f:
               async for line in in_f:
                   await out_f.write(line)
                   await asyncio.sleep(0.5)  # Simulate async operation

   async def main():
       await copy_file('input.txt', 'output.txt')

   asyncio.run(main())
```

</details>

24. **Асинхронный сон с пробуждением**

**Задача:** Напишите корутину, которая "спит" 3 секунды, затем "просыпается" и выводит сообщение.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def sleep_and_wake_up(seconds):
       await asyncio.sleep(seconds)
       print("Wake up!")

   async def main():
       await sleep_and_wake_up(3)

   asyncio.run(main())
   ```
</details>       

25. **Асинхронный цикл с условием**

**Задача:** Напишите асинхронный цикл, который выводит числа от 1 до 5 с задержкой 1 секунда, но прерывается, если введенное пользователем значение равно `stop`.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def async_cycle():
       for i in range(1, 6):
           user_input = await async_input(f"Iteration {i}. Enter 'stop' to exit: ")
           if user_input.lower() == 'stop':
               break
           await asyncio.sleep(1)

   async def main():
       await async_cycle()

   asyncio.run(main())
   ```
</details>       

----

### Умеренно сложные задачи

26. **Асинхронный пул задач**

**Задача:** Создайте пул задач, который выполняет асинхронные задачи с ограниченным количеством одновременно выполняющихся задач.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def task(semaphore, id, delay):
       async with semaphore:
           print(f"Task {id} started")
           await asyncio.sleep(delay)
           print(f"Task {id} finished")

   async def main():
       semaphore = asyncio.Semaphore(2)
       tasks = [task(semaphore, i, i) for i in range(1, 6)]
       await asyncio.gather(*tasks)

   asyncio.run(main())
   ```
</details>       

27. **Асинхронный счетчик с состоянием**

**Задача:** Создайте асинхронный счетчик, который увеличивает свое значение каждую секунду, но может быть сброшен в любой момент.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   class AsyncCounter:
       def __init__(self):
           self.count = 0

       async def increment(self):
           while True:
               self.count += 1
               print(self.count)
               await asyncio.sleep(1)

       async def reset(self):
           self.count = 0
           print("Counter reset")

   async def main():
       counter = AsyncCounter()
       increment_task = asyncio.create_task(counter.increment())
       await asyncio.sleep(3)
       await counter.reset()
       await asyncio.sleep(1)
       await increment_task

   asyncio.run(main())
   ```
</details> 

28. **Асинхронный кэш**

**Задача:** Реализуйте простой асинхронный кэш с ограниченным временем жизни для значений.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   class AsyncCache:
       def __init__(self):
           self.cache = {}

       async def get(self, key):
           if key in self.cache:
               return self.cache[key]
           return None

       async def set(self, key, value, ttl=5):
           self.cache[key] = value
           await asyncio.sleep(ttl)
           if key in self.cache:
               del self.cache[key]

   async def main():
       cache = AsyncCache()
       await cache.set('key1', 'value1', 2)
       print(await cache.get('key1'))  # Should print 'value1'
       await asyncio.sleep(3)
       print(await cache.get('key1'))  # Should print None

   asyncio.run(main())
   ```
</details>  

29. **Асинхронный пул подключений**
   
**Задача:** Создайте пул подключений, который ограничивает количество одновременных подключений к серверу.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   class ConnectionPool:
       def __init__(self, max_connections):
           self.semaphore = asyncio.Semaphore(max_connections)

       async def acquire(self):
           async with self.semaphore:
               yield

   async def task(pool, id):
       async with pool.acquire():
           print(f"Connection {id} acquired")
           await asyncio.sleep(1)
           print(f"Connection {id} released")

   async def main():
       pool = ConnectionPool(2)
       tasks = [task(pool, i) for i in range(5)]
       await asyncio.gather(*tasks)

   asyncio.run(main())
   ```
</details> 

30. **Асинхронный таймер**

**Задача:** Реализуйте асинхронный таймер, который выполняет задачу периодически с заданным интервалом.
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def periodic_task(interval, task_func):
       while True:
           await asyncio.sleep(interval)
           await task_func()

   async def task_func():
       print("Task executed")

   async def main():
       asyncio.create_task(periodic_task(2, task_func))
       await asyncio.sleep(6)

   asyncio.run(main())
   ```
</details> 

31. **Асинхронный логгер**

**Задача:** Создайте асинхронный логгер, который записывает сообщения в файл с задержкой.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import aiofiles

   async def async_logger(message, delay):
       await asyncio.sleep(delay)
       async with aiofiles.open('log.txt', mode='a') as f:
           await f.write(f"{message}\n")

   async def main():
       tasks = [async_logger(f"Log message {i}", i * 0.5) for i in range(5)]
       await asyncio.gather(*tasks)

   asyncio.run(main())
   ```
</details> 

32. **Асинхронный калькулятор**

**Задача:** Реализуйте асинхронный калькулятор, который вычисляет сумму, разность, произведение и частное двух чисел с задержкой.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def calculate(a, b, operation, delay):
       await asyncio.sleep(delay)
       if operation == 'add':
           return a + b
       elif operation == 'subtract':
           return a - b
       elif operation == 'multiply':
           return a * b
       elif operation == 'divide':
           return a / b

   async def main():
       result = await calculate(10, 5, 'add', 1)
       print(result)

   asyncio.run(main())
   ```

</details>    

33. **Асинхронный менеджер контекста**

**Задача:** Создайте асинхронный менеджер контекста, который выполняет некоторое действие при входе и выходе из контекста.
   
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   class AsyncContextManager:
       async def __aenter__(self):
           print("Entering async context")
           return self

       async def __aexit__(self, exc_type, exc_val, exc_tb):
           print("Exiting async context")

   async def main():
       async with AsyncContextManager():
           await asyncio.sleep(1)
           print("Inside async context")

   asyncio.run(main())
   ```

</details>   

34. **Асинхронный генератор чисел Фибоначчи**

**Задача:** Создайте асинхронный генератор, который выдает числа Фибоначчи с задержкой.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def fibonacci():
       a, b = 0, 1
       while True:
           await asyncio.sleep(1)
           yield a
           a, b = b, a + b

   async def main():
       async for num in fibonacci():
           if num > 10:
               break
           print(num)

   asyncio.run(main())
   ```
</details>

35. **Асинхронный веб-скрейпинг**

**Задача:** Напишите асинхронный скрипт, который скачивает содержимое нескольких веб-страниц параллельно.
   
<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import aiohttp

   async def fetch(session, url):
       async with session.get(url) as response:
           return await response.text()

   async def main():
       async with aiohttp.ClientSession() as session:
           urls = ['http://example.com', 'http://example.org', 'http://example.net']
           tasks = [fetch(session, url) for url in urls]
           results = await asyncio.gather(*tasks)
           for result in results:
               print(len(result))

   asyncio.run(main())
   ```
</details>       


36. **Асинхронный чат**

**Задача:** Создайте простой асинхронный чат, где несколько пользователей могут отправлять и получать сообщения.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import aiofiles

   messages = asyncio.Queue()

   async def send_message(username, message):
       await messages.put(f"{username}: {message}")

   async def receive_message():
       while True:
           message = await messages.get()
           print(message)
           messages.task_done()

   async def main():
       asyncio.create_task(receive_message())
       await send_message("User1", "Hello")
       await send_message("User2", "Hi there!")
       await asyncio.sleep(1)  # Allow messages to be processed

   asyncio.run(main())
   ```
</details>  

37. **Асинхронный прогресс-бар**

**Задача:** Реализуйте асинхронный прогресс-бар, который обновляется каждую секунду.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import sys

   async def progress_bar(total):
       for i in range(total + 1):
           percent = i / total * 100
           sys.stdout.write(f"\r[{'#' * i}{' ' * (total - i)}] {percent:.2f}%")
           sys.stdout.flush()
           await asyncio.sleep(1)
       sys.stdout.write("\n")

   async def main():
       await progress_bar(10)

   asyncio.run(main())
   ```
</details> 

38. **Асинхронный пулинг данных**

**Задача:** Создайте асинхронный скрипт, который периодически получает данные с сервера и обрабатывает их.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio
   import aiohttp

   async def fetch_data(session, url):
       async with session.get(url) as response:
           return await response.json()

   async def process_data(data):
       print("Processing data:", data)

   async def main():
       async with aiohttp.ClientSession() as session:
           url = 'http://example.com/data'
           while True:
               data = await fetch_data(session, url)
               await process_data(data)
               await asyncio.sleep(5)

   asyncio.run(main())
   ```
</details>

39. **Асинхронный сервер**

**Задача:** Напишите простой асинхронный сервер, который принимает соединения и отправляет ответ клиенту.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def handle_client(reader, writer):
       data = await reader.read(100)
       message = data.decode()
       addr = writer.get_extra_info('peername')
       print(f"Received {message} from {addr}")
       writer.write(data)
       await writer.drain()
       writer.close()

   async def main():
       server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
       addr = server.sockets[0].getsockname()
       print(f'Serving on {addr}')
       async with server:
           await server.serve_forever()

   asyncio.run(main())
   ```
</details>

40. **Асинхронный таск-менеджер**

**Задача:** Создайте асинхронный таск-менеджер, который управляет выполнением и отменой задач.

<details>       
<summary><b>Решение</b></summary> <br>

```python
   import asyncio

   async def long_task(id):
       print(f"Task {id} started")
       await asyncio.sleep(5)
       print(f"Task {id} finished")

   async def task_manager():
       tasks = [asyncio.create_task(long_task(i)) for i in range(3)]
       await asyncio.sleep(2)
       for task in tasks:
           task.cancel()
           try:
               await task
           except asyncio.CancelledError:
               print("Task cancelled")

   async def main():
       await task_manager()

   asyncio.run(main())
   ```
</details>

-------