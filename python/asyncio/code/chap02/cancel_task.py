import asyncio
import time
from asyncio import CancelledError
from util import delay

async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        print("Task not finished, checking again in a second.")
        await asyncio.sleep(1)  # this is async sleep which will block current coroutine (main()) but allows others to run DURING this 1 sec
        # time.sleep(1)         # this is a synchronous sleep which will block everything
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()
        
    try:
        await long_task
    except CancelledError:
        print('Our task was cancelled')

asyncio.run(main())