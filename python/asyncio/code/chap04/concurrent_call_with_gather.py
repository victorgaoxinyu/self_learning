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

# asyncio.run(async_main())
# asyncio.run(sync_main())
# asyncio.run(order_main())
# asyncio.run(except_main())
asyncio.run(handle_except_main())
