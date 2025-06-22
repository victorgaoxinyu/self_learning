import asyncio
from aiohttp import ClientSession
from util.async_timer import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    await asyncio.sleep(delay)
    print(f"[START] fetch_status: {url}")
    try:
        async with session.get(url) as result:
            print(f"[FETCHED] {url} with status {result.status}")
            return result.status
    except Exception as e:
        print(f"[EXCEPTION] {url} -> {e}")
        raise e
        # return f"Error: {e}"
    finally:
        print(f"[END] fetch_status: {url}")
