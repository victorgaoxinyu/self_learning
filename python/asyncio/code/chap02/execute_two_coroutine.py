import asyncio
from util.delay_functions import delay

async def add_one(number):
    return number + 1

async def hello_world_message():
    await delay(1)
    return 'Hello world'

async def main():
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)

asyncio.run(main())