import asyncio
from util import delay

async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Got a timeout")
        print(f'Was the task cancelled? {delay_task.cancelled()}')

asyncio.run(main())

async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Task took longer than five seconds, keep running")
        result = await task
        print(result)

asyncio.run(main())