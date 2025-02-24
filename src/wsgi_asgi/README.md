# WSGI & ASGI

## Что такое WSGI?
`WSGI` — это интерфейс, который соединяет веб-сервер и веб-приложение на Python. 
Он стандартизирует взаимодействие между сервером и приложением.

### Основные концепции WSGI
#### Веб-сервер:
**Веб-сервер** принимает `HTTP`-запросы от клиентов (браузеров, мобильных приложений и т.д.) и передает их 
веб-приложению через `WSGI`.
Примеры веб-серверов, поддерживающих `WSGI`: `Gunicorn`, `uWSGI`, `mod_wsgi` (для `Apache`).

#### Веб-приложение:
**Веб-приложение** — это код, который обрабатывает запросы и возвращает ответы. 
В контексте `WSGI`, веб-приложение — это вызываемый объект (функция или класс), 
который принимает два аргумента: `environ` и `start_response`.

#### Аргументы WSGI:
**environ**: Словарь, содержащий информацию о запросе, такую как метод запроса (`GET`, `POST`), заголовки, путь и т.д.
**start_response**: Вызываемая функция, которую веб-приложение использует для отправки `HTTP`-статуса и заголовков ответа.

```python
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [b'<html><body><h1>Hello, WSGI!</h1></body></html>']

```

### Как работает WSGI-сервер и как он взаимодействует с приложением?
**WSGI-сервер** получает `HTTP`-запрос, преобразует его в Python-объекты и передает в `WSGI`-приложение. 
Ответ от приложения возвращается обратно в виде `HTTP`-ответа.

```python
def run_wsgi_app(app, environ):
    def start_response(status, response_headers):
        # Сохраняем статус и заголовки для последующей отправки
        nonlocal status_line, headers
        status_line = status
        headers = response_headers

    # Вызываем WSGI-приложение
    response_body = app(environ, start_response)

    # Формируем HTTP-ответ
    response = [f'HTTP/1.1 {status_line}'.encode()]
    for header in headers:
        response.append(f'{header[0]}: {header[1]}'.encode())
    response.append(b'')
    response.extend(response_body)

    return response

# Пример использования
environ = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    # Другие необходимые ключи
}

response = run_wsgi_app(simple_app, environ)
print(b'\r\n'.join(response).decode())
```

### В чем основное отличие между WSGI-приложением и обычной Python-функцией?
`WSGI`-приложение — это `Python`-функция, которая принимает два аргумента: `environ` (среда запроса) 
и `start_response` (функция для формирования ответа).

```python
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello, World!"]
```

## Что такое ASGI и чем он отличается от WSGI?
`ASGI` — это асинхронный интерфейс между сервером и приложением, поддерживающий не только `HTTP`, 
но и асинхронные протоколы (например, `WebSocket`). `WSGI` поддерживает только синхронные запросы.

### Какие проблемы, связанные с асинхронностью, решает ASGI по сравнению с WSGI?
`ASGI` поддерживает обработку асинхронных операций и многопротокольные коммуникации, 
такие как `WebSocket` и `keep-alive` соединения.

### Как запустить asgi / wsgi приложение?
- `WSGI`-приложения запускаются через синхронные `WSGI`-серверы, такие как `Gunicorn`.
- `ASGI`-приложения требуют асинхронных серверов, таких как `Uvicorn` или `Daphne`.