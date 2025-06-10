from multiprocessing import Process, Value, Array
from concurrent.futures import ProcessPoolExecutor
import asyncio

def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_value_with_lock(shared_int: Value):
    # shared_int.get_lock().acquire()
    # shared_int.value = shared_int.value + 1
    # shared_int.get_lock().release()
    with shared_int.get_lock():
        shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


def increase_once():
    integer = Value('i', 0)
    integer_array = Array('i', [0, 1])

    procs = [Process(target=increment_value, args=(integer, )),
             Process(target=increment_array, args=(integer_array, ))]

    [p.start() for p in procs]
    [p.join() for p in procs]

    print(integer.value)
    print(integer_array[:])  # [1, 2]


def increase_twice():
    for _ in range(100):
        integer = Value('i', 0)
        # procs = [
        #     Process(target=increment_value, args=(integer, )),
        #     Process(target=increment_value, args=(integer, )),
        # ]

        procs = [
            Process(target=increment_value_with_lock, args=(integer, )),
            Process(target=increment_value_with_lock, args=(integer, )),
        ]


        [p.start() for p in procs]
        [p.join() for p in procs]
        print(integer.value)

        assert(integer.value == 2)  # Non-determinism! not always 2, sometimes 1


if __name__ == "__main__":
    # increase_once()
    # increase_twice()

