### Intro to multiprocessing pkg

#### basic usage

```python
task = Process(func, args)
task.start()
task.join()
```

- call start and join for every process
- dont know which will finish first.

#### process pool

```
with Pool() as process_pool:
  task_1 = process_pool.apply(func, args)

with Pool() as process_pool:
  task_2 = process_pool.apply_async(func, args)
  print(task_2.get())
```



- `apply` method is a blocking method

- `apply_async` is non blocking, so will multi-process in parallel

  - but `.get()` is blocking!

  - cannot achieve similar effect as `asyncio.as_completed`

#### Process pool Executor

- `Executor` abstract class
  - `submit`
  - `map`
- `ProcessPoolExecutor` and `ThreadPoolExecutor`

#### Process pool with asyncio

- get a EventLoop and call `run_in_executor(process_pool, callable)`

#### MapReduce model

- 将大型数据集划分成较小的块, mapping
- 解决了每个子集的问题再归约成最终答案, reducing