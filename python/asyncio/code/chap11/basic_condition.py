import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    while True:
        print("Waiting for condition lock...")
        async with condition:
            print("Acquired lock, releasing and waiting for condition")
            await condition.wait()  # 等待事件触发
            print("Condition event fired, re-acquiring lock and doing work...")
            await asyncio.sleep(1)
        
        print("Work finished, lock released")


async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print("fire event: About to notify, acquiring condition lock...")
        async with condition:
            print("fire event: Lock acquired, notifying all workers.")
            condition.notify_all()  # 一旦调用notify all，worker任务就会唤醒 ^
        
        print("fire event: Notification finished, releasing lock")


async def main():
    condition = Condition()

    asyncio.create_task(fire_event(condition))

    await asyncio.gather(do_work(condition), do_work(condition))


asyncio.run(main())


