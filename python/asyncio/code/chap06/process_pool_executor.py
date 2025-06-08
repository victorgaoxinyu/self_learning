import time
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List

from multiprocess_intro import count

def basic_process_pool():
    with ProcessPoolExecutor() as process_pool:
        # numbers = (1, 3, 5, 22, 100000000)
        numbers = (100000000, 1, 3, 5, 22)  # if we put larger number at the beginning
                                            # we need wait until it finish, then output other result
                                            # not as fast as asyncio.as_completed
        for res in process_pool.map(count, numbers):
            print(res) 


async def process_pool_with_asyncio():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        # numbers = (1, 3, 5, 22, 100000000)
        numbers = (100000000, 1000000, 30000000, 500000, 22) 
        calls: List[partial[int]] = [partial(count, num) for num in numbers]

        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))
        
        results = await asyncio.gather(*call_coros)
        for result in results:
            print(result)


if __name__ == "__main__":
    # basic_process_pool()
    asyncio.run(process_pool_with_asyncio())