### Goal
- Create a server that can handle multi users' request, using one thread.

### Blocking Sockets

```
 Client side                             Server side
 --------                              ---------------
| Client |  -- request to connect --> | Server Socket |
 --------                              ---------------
    A                                        |
    |                                        | establish client socket
    |                                        V
    |      read and write              ---------------
    --------------------------------> | Client socket |
                                       ---------------
```
When more than one client connected, one client could cause others to wait for it to send data.


### Non-blocking socket
- set both client and server to use non-blocking.
- this will increase cpu usage as it will keep iter and catch exceptions.

### Use selector
- provide OS a list of sockets we want to monitor for events, instead of constantly checking each socket.
- abstract base class `BaseSelector`
  - `registration`: register the socket we care with selector, and tell it which wevents we cares
  - `select`: block until an event has happened, and then return a list of sockets that ready for processing

### Use asyncio event loop
- `sock_accept`, `sock_recv` and `sock_sendall`

```python

# connection, address = server_socket.accept()
connection, address = await loop.sock_accept(socket)

# data = event_socket.recv(1024)
data = await loop.sock_recv(socket)

# event_socket.send(data)
success = await loop.sock_sendall(socket, data)
```

### Shutting down gracefully
- in UNIX, listen to `SIGINT` and `SIGTERM` and add delay to complete echo task.
- use `add_signal_handler` method.

### Waiting for pending tasks to finish
- 在关闭之前，给echo任务几秒钟的时间以保持运行
  - 方法1: 将所有echo任务包装在wait_for中。
```python
async def await_all_tasks():
    tasks = asyncio.all_tasks()
    [await task for task in tasks]

async def main():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(await_all_tasks()))  # lambda这里确保await_all_tasks 在信号发生时运行， 而非注册时
```
  - Flaws:
    - "Exception was never retrieved"
  - 方法2:
```python
class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()

async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # a timeout error here
            pass

loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, shutdown)

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
```