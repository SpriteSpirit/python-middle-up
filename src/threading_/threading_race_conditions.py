import threading
import time

counter = 0


def increment():
    global counter

    for i in range(10000):
        temp = counter
        time.sleep(0.000001)  # Искусственная задержка
        counter = temp + 1


# создание 2х потоков
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)
thread3 = threading.Thread(target=increment)
thread4 = threading.Thread(target=increment)

# запуск потоков
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# ожидание завершения потоков
thread1.join()
thread2.join()
thread3.join()
thread4.join()

print(f"Итоговое значение {counter=}")
