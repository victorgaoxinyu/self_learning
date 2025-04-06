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
- 