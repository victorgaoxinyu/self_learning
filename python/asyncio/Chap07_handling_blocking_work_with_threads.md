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

- `from threading import Lock, Thread`

Reentrancy

- 可重入锁
  - 同一个线程可以多次获得这种锁
  - `from threading import Rlock`

Dead lock

- 鸵鸟算法
  - 是一个忽略潜在问题的一种算法策略，这种策略对计算机程序可能出现的问题采取无视态度。鸵鸟算法的使用前提是，问题出现的概率很低。
- 始终以相同顺序获取锁，方法A和B都先获取锁A再获取锁B
- 重构锁，只使用一个锁

### Eventloop in single thread

Tkinter

### Using thread for CPU bounded task

hashlib



