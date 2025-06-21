### Theading!

- GIL
- During I/O operation, GIL is released since I/O operations are OS level sys calls

Multi-thread echo server

- if we Ctrl-C main thread, any existing client can still communicate with server
- those threads are keep running
- use `thread.deamon = True` to setup deamon thread.
  - problem is when thread stop, we cannot have clean or close logic

### Using thread with asyncio

- `ThreadPoolExecutor`
- theadpool with asyncio, this does not yield performance improvement comparing with just using threadpool. But this allows us able to do other things while waiting for all coroutine to finish.
- `loop.run_in_excutor(executor, callable)`
  - executor can be None and default to a `ThreadPoolExecutor`
  - can use `asyncio.to_thread` to further simplify putting work on default thread pool executor.

### Lock, data sharing and dead lock in threading

