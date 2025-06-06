import sys
from pathlib import Path
import asyncio, signal
from asyncio import AbstractEventLoop
from typing import Set

sys.path.append(str(Path(__file__).parent.parent))
from util.delay_functions import delay

def cancel_tasks():
    print("Got a SIGINT")
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]

async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, cancel_tasks)

    await delay(10)

asyncio.run(main())