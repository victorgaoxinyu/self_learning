import asyncio
import os
import tty
from collections import deque
from async_stdin_reader import create_stdin_reader, read_line
from message_storing import MessageStore
from escape_functions import *


async def sleep(delay: int, message_store: MessageStore):
    await message_store.append(f"Starting delay {delay}")
    await asyncio.sleep(delay)
    await message_store.append(f"Finished delay {delay}")


async def main():
    tty.setcbreak(sys.stdin)
    os.system("clear")
    rows = move_to_bottom_of_screen()

    async def redraw_output(items: deque):
        save_cursor_positions()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_positions()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()

    while True:
        line = await read_line(stdin_reader)
        if line != '':
            delay_time = int(line)
            asyncio.create_task(sleep(delay_time, messages))

asyncio.run(main())
