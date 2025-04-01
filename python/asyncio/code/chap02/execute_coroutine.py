import asyncio

async def coroutine_add_one(number):
    return number + 1

result = asyncio.run(coroutine_add_one(1))

print(result)