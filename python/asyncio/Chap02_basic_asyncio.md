### Coroutine
- regular python function return the value
- coroutine python function return corutine object, does not execute the function
- need to explicitly execute that in event loop

Use await to pause execution
- await + coroutine (actually should be `awaitable` object)


```python
import asyncio

async def add_one(number):
    return number + 1

async def main():
    one_plus_one = await add_one(1)
    two_plus_one = await add_one(2)

    print(one_plus_one)
    print(two_plus_one)

asyncio.run(main())
"""
main() -> pause main() -> resume main() -> pause main() -> resume main()
           add_one(1)                       add_one(2)
"""
```
so far same to normal python execution.

### Use task/event loop to achieve parallelism


### Cancel task and timeout
- Use `cancel` method to cancel any task object, and throw `CancelledError`
- Use `asyncio.wait_for` to setup timeout.
- Use `asyncio.shield` to prevent from timeout.

### Task, Coroutine, future and awaitable
Future
- 包含你希望在未来某个时间点获得但是目前可能还不存在的值
- 通常来说创建future的时候没有任何值，因为他还不存在
- 一旦得到一个结果，就可以设置future的值
- future 用在await表达中
  - 暂停， 直到future有一个可供使用的值集，一旦有了一个值，唤醒。
- 类似JS中Promise，以及Java中的completable future.
```python
from asyncio import Future

my_future = Future()
print(my_future.done())
my_future.set_result(42)

print(my_future.done(), my_future.result())
```
#### Future, task and coroutine
- `Task` inherit from `future`

awaitable
- abstract base class
- anything have `__await__` implemented can be used in `await` 
```
  awaitable
   /     \
corotine future
           \
           task
```
#### Pitfalls，常见两个错误
- 尝试在不使用多处理的情况下，在任务或者协程中运行CPU密集型代码
- 使用阻塞I/O密集型API而不使用多线程。
  - 通常来说大多数API都是blocking的，无法和asyncio一起使用
  - 需要使用支持协程，并利用nonblocking socket的库
  - 或者使用线程池来配合blocking库使用

### Manually create and access event loop

Create event loop
```python
import asyncio

async def main():
    await asyncio.sleep(1)

loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()  # 关闭事件循环，释放资源
                  # 写在finally中，这样任何exception都不会阻止我们关闭。
```

Access event loop
```python
import asyncio

def call_later():
    print("I am being called in the future!")

async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

asyncio.run(main())
```


### Debug
- Use `asyncio.run(main(), debug=True)` to enable debug mode
- use `loop.slow_callback_duration = .250` to adjust threshold.