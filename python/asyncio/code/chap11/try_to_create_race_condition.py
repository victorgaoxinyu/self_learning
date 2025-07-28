import asyncio


counter = 0


async def increment():
    global counter
    await asyncio.sleep(0.01)
    counter = counter + 1


async def main():
    global counter
    for _ in range(100):
        tasks = [asyncio.create_task(increment()) for _ in range(100)]
        await asyncio.gather(*tasks)

        print(f"Counter is {counter}")

        assert counter == 100
        counter = 0


# asyncio.run(main())


async def increment_with_assign():
    global counter
    tmp = counter
    tmp = tmp + 1
    await asyncio.sleep(0.01)  # here yield control, and other tasks run now
    counter = tmp


async def main_with_assign():
    global counter
    for _ in range(100):
        tasks = [asyncio.create_task(increment_with_assign()) for _ in range(100)]
        await asyncio.gather(*tasks)

        print(f"Counter is {counter}")

        assert counter == 100
        counter = 0


asyncio.run(main_with_assign())
