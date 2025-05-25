import logging
import asyncio
import aiohttp
from aiohttp import ClientSession

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed, fetch_status, delay

# Async
@async_timed()
async def async_main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_code = await asyncio.gather(*requests)
        print(status_code)
    

# Sync
@async_timed()
async def sync_main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        status_codes = [await fetch_status(session, url) for url in urls]
        print(status_codes)


# Order
# gather return result in pass-in order desipte they might finish in a different order
async def order_main():
    results = await asyncio.gather(delay(3), delay(1))
    print(results)  # [3, 1]


# Exception handling using `return_excaptions`

@async_timed()
async def except_main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*tasks)
        print(status_codes)


@async_timed()
async def handle_except_main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'All results: {results}')
        print(f'Finished successfully: {successful_results}')
        print(f'Threw exceptions: {exceptions}')

@async_timed()
# usage of as_completed
# this also have better exception handling
async def process_req_when_finish():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)

@async_timed()
# as_completed timeout
async def process_req_with_timeout():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
            fetch_status(session, 'https://www.example.com', 10),
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=9):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('Time out error')
        
        for task in asyncio.tasks.all_tasks():
            print(task)

@async_timed()
async def finer_grained_control_with_wait():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


@async_timed()
async def exception_handling_with_wait():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad', 10)

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request),
        ]

        # ALL_COMPLETED: asyncio.wait等到一切都完成后才会返回
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


@async_timed()
async def exception_handling_with_wait_first_exception():
    # 任何任务抛出异常，wait立即返回
    # 完成集合(done)包含所有完成的协程以及任何有异常的协程
    # 挂起(pending)可能为空，也可能存在仍在运行的任务
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'python://bad.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3))
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Result got an exception", exc_info=done_task.exception())
        
        for pending_task in pending:
            pending_task.cancel()

# asyncio.run(async_main())
# asyncio.run(sync_main())
# asyncio.run(order_main())
# asyncio.run(except_main())
# asyncio.run(handle_except_main())
# asyncio.run(process_req_when_finish())
# asyncio.run(process_req_with_timeout())
# asyncio.run(finer_grained_control_with_wait())
# asyncio.run(exception_handling_with_wait())
asyncio.run(exception_handling_with_wait_first_exception())