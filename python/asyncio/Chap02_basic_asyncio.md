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


