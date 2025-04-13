import asyncio
import signal

async def crash_task():
    print("Crash task started")
    await asyncio.sleep(1)
    raise ValueError("Intentional crash!")  # 模拟任务抛出异常

async def normal_task():
    print("Normal task running")
    await asyncio.sleep(2)
    print("Normal task completed")

async def await_all_tasks():
    tasks = asyncio.all_tasks()
    [await task for task in tasks]  # 等待所有任务，但不会处理异常

async def main():
    loop = asyncio.get_event_loop()
    
    # 注册信号处理器（Ctrl+C触发）
    loop.add_signal_handler(
        signal.SIGINT,
        lambda: asyncio.create_task(await_all_tasks())
    )
    
    # 启动一个会崩溃的任务和一个正常任务
    asyncio.create_task(crash_task())
    asyncio.create_task(normal_task())
    
    # 保持主程序运行
    await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())