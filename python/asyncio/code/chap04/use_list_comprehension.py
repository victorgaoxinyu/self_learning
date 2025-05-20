import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed, delay

@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    # This is incorrect
    # coz await is called when each task
    # [await asyncio.create_task(delay(seconds)) for seconds in delay_times]
    
    # This is correct
    # split task creation and await
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]

asyncio.run(main())