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
- 会话级别超时
  - 整个session（连接，发送，接受）
  - 连接
- 请求级别超时
  - 当前单个请求
```
用户请求 → [网关(全局1s)] → [服务A(默认300ms)] → [服务B(关键路径50ms)]
                                      ↘ [服务C(非关键路径100ms)]
```

### asyncio.gather used for awaitables
`gather` function keeps result ordering determinstic.
Implementaion key mechanics:
- create a results list that preserves input order
- each coroutine is cheduled and given an index
- when a corotine finishes, result is place in `self._result[index]` 
```py
# simplified source code

class _GatheringFuture(asyncio.Future):
  def __init__(self, futures, loop):
    super().__init__(loop=loop)
    self._futures = futures
    self._results = [None] * len(futures)
    self._unfinished_count = len(futures)

    for i, fut in enumerate(futures):
      fut = asyncio.ensure_future(fut, loop=loop)
      fut.add_done_call_batch(self._make_callback(i))
  
  def _make_callback(self, index):
    def  _callback(fut):
      if self.cancelled():
        return
      try:
        result = fut.result()
      except Exception as exc:
        self.set_exception(exc)
        return
      self._results[index] = result
      self._unfinished_count -= 1
      if self._unfinished_count == 0:
        self.set_result(self._results)
    return _callback

```

### handle exception

- `asyncio.gather(*tasks, return_exceptions=True)`

x