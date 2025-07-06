import sys
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from util.delay_functions import delay

async def main():
    while True:
        delay_time = input("Enter a time to sleep: ")
        asyncio.create_task(delay(int(delay_time)))
        # await asyncio.sleep(0)  # work around but still not work properly
                                  # `yielding to the event loop`

# What we want
# 创建一个在等待用户输入时，不会阻塞事件循环的命令行应用程序
# check async_stdin_reader.py

from async_stdin_reader import create_stdin_reader

async def use_stdin_reader():
    stdin_reader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))




# asyncio.run(main())
asyncio.run(use_stdin_reader())