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

### Shared Data and Lock

- shared memory objects

  - fairly complicated 
  - try to avoid unless really neccessary
  - support value and array
    - int/float

- Race condition

  - ```
    # Avoid race condition
    Process 1 																								Process 2
    read   shared_data = 0           shared_data = 0
    write  shared_data = 0 + 1       shared_data = 1					read  shared_data = 1
                                     shared_data = 2          write shared_data = 1 + 1
                                     
    # Race condition
    Process 1 																								Process 2
    read   shared_data = 0           shared_data = 0          read shared_data = 0
    write  shared_data = 0 + 1       shared_data = 1					write  shared_data = 0 + 1	
    ```

  - things implemented in C in python are atomic and thread-safe

    - ```
      x = 1, y = x
      list.append(x)
      list.pop()
      list.__setitem__, list.__getitem__
      dict.__setitem__, dict__getitem__, dict.get()
      key in dict
      set.add(x)
      set.remove(x)
      x in set
      len(), id(), type()
      ```

    - Not atomic

      - ```
        x += 1
        list[idx] += 1
        ```

- Lock to prevent race conditions

  - ```
    with shared_int.get_lock():
        # add value
    ```

### Multiprocess and multi event loop



