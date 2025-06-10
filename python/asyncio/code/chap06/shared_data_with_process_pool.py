from multiprocessing import Process, Value, Array
from concurrent.futures import ProcessPoolExecutor
import asyncio

shared_counter: Value

def init(counter: Value):
    global shared_counter
    shared_counter = counter

def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def share_data_with_process_pool():
    counter = Value('d', 0)
    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        loop = asyncio.get_running_loop()
        call_coros = []
        for _ in range(10):
            call_coros.append(loop.run_in_executor(pool, increment))

        await asyncio.gather(*call_coros)
        print(counter.value)  # always be 10

if __name__ == "__main__":
    # increase_once()
    # increase_twice()
    asyncio.run(share_data_with_process_pool())
