import sys
from pathlib import Path
import asyncio
import aiohttp
from aiohttp import ClientSession

sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed

@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    ten_millis = aiohttp.ClientTimeout(total=.01)
    # get请求超时10ms
    async with session.get(url, timeout=ten_millis) as result:
        return result.status

@async_timed()
async def main():
    # 客户端会话级别超时，总超时1s，连接超时100ms
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = "https://www.example.com"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")


# asyncio.run(main())