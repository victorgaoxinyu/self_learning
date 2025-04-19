## Concurrent web requests

### Goal
- learn `aiohttp`
  - 学习如何获取数百个url的列表，并同时运行所有请求
  - asyncio一次性运行协程的API
  - 请求设置超时
  - 根据其他请求执行情况来取消一组正在执行的请求

### async context manager
- context manager works for synchronous resources
```python
with open('example.txt') as file:
    lines = file.readlines()
```
- context manager works for async
```python
async with open ...
# async context manager are classes that implement 2 special coroutine methods
# __aenter__, and __aexit__
```

### Web request using aiohttp
- connection pool
- by default ClientSession can create 100 connection. Create aiohttp TCPConnector instance to modify default value.

### aiohttp Timeout

