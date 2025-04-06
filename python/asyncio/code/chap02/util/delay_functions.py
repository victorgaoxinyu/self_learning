import asyncio

async def delay(seconds):
    print(f'sleeping for {seconds} second(s)')
    await asyncio.sleep(seconds)
    print(f'finished sleeping for {seconds} second(s)')
    return seconds

