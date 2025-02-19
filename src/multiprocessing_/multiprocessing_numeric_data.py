import concurrent.futures
import json
import multiprocessing
import time

from src.multiprocessing_.generate_data import generate_data


def process_number(number: int):
    """
    Вычисляет факториал числа.

    :param number: Число, для которого нужно вычислить факториал.
    :return: Факториал числа.
    """

    result = 1

    for i in range(1, number + 1):
        result *= i

    return result


# Вариант А - Использование пула потоков с concurrent.futures
def parallel_process_threads(data: list) -> list:
    """
    Вычисляет факториалы чисел в параллельном режиме с использованием пула потоков.

    :param data: Список чисел для вычисления факториалов.
    :return: Список факториалов чисел.
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))


# Вариант Б - Использование multiprocessing.Pool с пулом процессов, равным количеству CPU
def parallel_process_pool(data: list) -> list:
    """
    Вычисляет факториалы чисел в параллельном режиме с использованием пула процессов.

    Если процессор имеет 4 физических ядра без Hyper-Threading, multiprocessing.cpu_count() вернет 4.
    Если процессор имеет 4 физических ядра с поддержкой Hyper-Threading,
    где каждое физическое ядро может выполнять два потока одновременно, multiprocessing.cpu_count() вернет 8.

    :param data: Список чисел для вычисления факториалов.
    :return: Список факториалов чисел.
    """

    # processes=multiprocessing.cpu_count() - возвращает количество CPU-ядер, доступных в системе (явное указание)
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(process_number, data)


# Вариант В - Создание отдельных процессов с использованием multiprocessing.Process
# и очередей (multiprocessing.Queue) для передачи данных


def process_worker(queue: multiprocessing.Queue, data: list) -> None:
    """
    Выполняет вычисление факториалов в отдельном процессе и помещает результаты в очередь.

    :param queue: Очередь для передачи результатов.
    :param data: Список чисел для вычисления факториалов.
    """

    for number in data:
        result = process_number(number)
        queue.put(result)


def parallel_process_queue(data: list) -> list:
    """
    Вычисляет факториалы чисел с использованием отдельных процессов и очередей.

    :param data: Список чисел для вычисления факториалов.
    :return: Список факториалов чисел.
    """

    # кол-во процессов == кол-ву ядер процессора
    num_processes = multiprocessing.cpu_count()
    # размер фрагмента данных для обработки одним процессом.
    chunk_size = len(data) // num_processes
    queues = [multiprocessing.Queue() for i in range(num_processes)]
    processes = []

    for i in range(num_processes):
        # начало текущего фрагмента данных, умножая индекс процесса на размер фрагмента
        start = i * chunk_size
        # конец текущего фрагмента данных
        end = start + chunk_size if i < num_processes - 1 else len(data)
        # создание и запуск процесса для обработки текущего фрагмента данных.
        process = multiprocessing.Process(
            target=process_worker, args=(queues[i], data[start:end])
        )
        processes.append(process)
        process.start()

    results = []

    for process in processes:
        # основной процесс будет ждать, пока каждый дочерний процесс завершится, прежде чем продолжить выполнение
        process.join()

    for queue in queues:
        while not queue.empty():
            results.append(queue.get())

    return results


# Сравнение производительности
def performance_comparison(data: list, conclusion: str = None) -> dict:
    parallel_processes_variants = {
        "single_thread": lambda data: [process_number(num) for num in data],
        "parallel_process_threads": parallel_process_threads,
        "parallel_process_pool": parallel_process_pool,
        "parallel_process_queue": parallel_process_queue,
    }

    results = {}

    for name, func in parallel_processes_variants.items():
        start_time = time.time()
        func(data)
        execution_time = time.time() - start_time
        results[name] = execution_time

    print("Время выполнения: ")
    for name, time_spent in results.items():
        print(f"{name}: {time_spent:.6f} сек")

    print(f"\n{conclusion}")

    return results


# Сохранение результатов
def save_results(results: dict, filename="results.json") -> None:
    """
    Сохраняет результаты в JSON-файл.

    :param results: Словарь с результатами.
    :param filename: Имя JSON-файла.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)


conclusion = """Вывод:
1. Характер задачи (CPU-bound vs. I/O-bound)
Факториал — это CPU-bound задача (интенсивная по вычислениям).
Потоки (Threads) в Python неэффективны для CPU-bound задач из-за Global Interpreter Lock (GIL), 
который заставляет потоки выполняться последовательно, даже на многопроцессорных системах. 
Поэтому parallel_process_threads работает медленнее, чем однопоточный вариант 
(дополнительные накладные расходы на управление потоками).

2. Накладные расходы на создание процессов
Мультипроцессинг (Processes) создает отдельные процессы с собственным интерпретатором Python и памятью. 
Это требует времени и ресурсов. 
Для маленьких данных накладные расходы на создание процессов и передачу данных между 
ними могут превысить выигрыш от параллелизма. Данные слишком малы, чтобы процессы успели "раскрыть потенциал".

3. Сравнение пула процессов (Pool) и очередей (Queue)
multiprocessing.Pool оптимизирован для задач "разделяй и властвуй", автоматически распределяя данные между 
процессами. Он эффективнее ручного управления процессами через Process и Queue.
Ручное управление процессами (вариант с очередями) добавляет дополнительные сложности и накладные расходы, 
что объясняет его самую низкую производительность.

4. Когда процессы выигрывают?
Процессы покажут преимущество, если:
   - Данные очень большие (например, 10⁵ элементов).
   - Вычисления для каждого элемента достаточно тяжелые (например, факториал числа 1000).
"""

if __name__ == "__main__":
    generated_data = generate_data(50)
    performance_results = performance_comparison(generated_data, conclusion=conclusion)

    save_results(performance_results)
