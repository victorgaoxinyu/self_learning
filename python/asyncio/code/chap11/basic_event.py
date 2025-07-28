import asyncio
import functools
from asyncio import Event


def trigger_event(event):
    event.set()  # set 将Event内部标志设置成True，并通知所有等待事件发生的人


async def do_work_on_event(event):
    print('Waiting for event...')
    await event.wait()  # this is blocking until event.set() is called
    print('Performing work!')
    await asyncio.sleep(1)
    print('Finished work')
    event.clear()  # if we call event.wait() again, it will block again


async def main():
    event = asyncio.Event()
    # asyncio.get_running_loop().call_later(5, functools.partial(trigger_event, event))
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))


asyncio.run(main())