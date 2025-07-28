import sys
from pathlib import Path
import asyncio
from asyncio import Lock
sys.path.append(str(Path(__file__).parent.parent))
from util.delay_functions import delay

async def a(lock: Lock):
    print('Coroutine `a` waiting to get the lock')
    async with lock:
        print('Corotine `a` is in the critical section')
        await delay(2)
    
    print('Corotine `a` released the lock')


async def b(lock: Lock):
    print('Coroutine `b` waiting to get the lock')
    async with lock:
        print('Corotine `b` is in the critical section')
        await delay(2)
    
    print('Corotine `b` released the lock')


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))

asyncio.run(main())