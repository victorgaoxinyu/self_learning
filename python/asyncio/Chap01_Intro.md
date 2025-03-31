
### I/O intensive and CPU intensive
```python
import requests
response = requests.get('https://www.example.com')  # I/O intensive web request

items = response.header.items()
headers = [f'{key}: {header}' for key, header in items]  # CPU intensive

formatted_headers = '\n'.join(headers)  # CPU intensive

with open('headers.txt', 'w') as f:
    f.write(formatted_headers)  # I/O intensive
```

### Concurrent and Parallel
- Concurrent: at the same time, only one task is running
- Parallel: at the same time, more than one tasks are running

### Preemptive multitasking and Cooperative Multitasking
- Preemptive multitasking: handled by OS
- Cooperative multitasking: handled by software

asyncio 使用协同多任务来实现并发，当程序达到可以等待一段时间以返回结果的时间点的时候，在代码中显式的标记他。这允许其他代码在等待结果返回后台时运行。

### Process and Thread
- Process: 进程，其他应用程序无法访问的内存空间和引用程序运行状态， PID
- Thread: 线程，轻量级进程，操作系统可以管理的最小结构，共享创建进程的内存。

```
|----父进程----|
|    Memory   |
|      |      |
|      v      |
| Main Thread |
```

### Global Interpreter Lock, GIL
- 当I/O操作发生的时候，GIL被释放，我们可以使用多线程来执行并发工作
- 不适用CPU intensive task
  - there are special cases, will discuss later

### Asyncio and GIL
- asyncio利用I/O操作释放GIL来提供并发性，即使只有一个线程也是如此。
- 使用asyncio的时候，创建了协程对象 Coroutine.
- python对于协程的实现是通过generator
```python
def consumer():
    r = ''
    while True:
        n = yield r
        if not n :
            return
        print(f'[CONSUMER] Consuming {n}')
        r = f'200 OK from iter {n}'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print(f'[PRODUCER] Producing {n}')
        r = c.send(n)
        print(f'[PRODUCER] Consumer return: {r}')
    
    c.close()

c = consumer()
produce(c)
```
consumer函数是一个generator，把consumer传入produce以后：
1. 调用c.send(None) 或者 next(c) 启动generator
2. 一旦生产了东西， 通过c.send(n) 切换到consumer执行
3. consumer 通过 yield 拿到消息，处理，又通过yield把结果传回
4.  produce拿到consumer处理的结果，继续生产下一条消息
5.  produce决定不生产了，通过c.close() 关闭consumer，过程结束

```python
# Another example of two-way communication
def interactive_generator():
    print("Generator started")
    x = yield "Ready"     # First yield (sends "Ready", then pauses to receive)
    print(f"Received: {x}")
    y = yield f"Got {x}"  # Second yield (sends "Got x", then pauses)
    print(f"Received: {y}")
    yield f"Final: {y}"

# Start the generator (must use `next()` or `send(None)` first)
print(gen.send(None))  # Output: "Ready" (generator runs until first yield)

# Send a value into the generator (resumes execution)
print(gen.send(10))    # Output: "Got 10" (x = 10 inside generator)

# Send another value
print(gen.send(20))    # Output: "Final: 20" (y = 20 inside generator)
```