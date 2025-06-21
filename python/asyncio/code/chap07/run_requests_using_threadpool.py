import sys
import time
from pathlib import Path
import functools
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed, delay


def get_status_code(url) -> int:
    response = requests.get(url)
    return response.status_code

# using `to_thread` coroutine to further simplify the code
@async_timed()
async def run_with_asyncio_to_thread():
    urls = ['https://www.example.com' for _ in range(1000)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


@async_timed()
async def run_theadpool_with_asyncio():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        urls = ['https://www.example.com' for _ in range(1000)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

def run_with_basic_threadpool():

    start = time.time()

    with ThreadPoolExecutor() as pool:
        urls = ['https://www.example.com' for _ in range(1000)]
        results = pool.map(get_status_code, urls)
        for result in results:
            print(result)

    end = time.time()

    print(f"finished in {end - start:.4f} second(s)")


if __name__ == "__main__":
    # run_with_basic_threadpool()
    # asyncio.run(run_theadpool_with_asyncio())
    asyncio.run(run_with_asyncio_to_thread())

