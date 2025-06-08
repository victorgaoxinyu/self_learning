### Use connection pool to implement concurrent search/query

- naively using `asyncio.gather` to run multiple queries at the same time will get exception

  - ```shell
    asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress	
    ```

- we need connection pool

  - ```
    instance(s)  --- connection pool --- DB
    ```

  - connection pool size is not the larger the better

    - Little's Law
      - pool size ~= (Expected Concurrent Requests * Average DB response Time) / Target response Time.



### Managing Transaction with asyncpg

ACID, Atomic, Consistent, isolated, durable.

- use connection.transaction async context manager
  - if error, fallback
  - if success, submit
- nested transaction
  - check point!
- Manually managing transaction
  - execute customised code when rolling back
  - different roll back conditions
  - `transaction.start(), transaction.rollback(), transaction.commit()`

### Async generator and streaming result

- asyncpg supports cursor
  - `async for` use with `async_generator`
- move forward and fetch 
  - `cursor.forward`, `cursor.fetch`
  - usually only forward
  - 2 directional -> DECLARE ... SCROLL CURSOR
- async generator
  - `take`
  - add a counter in async for loop, break when exceed threshold

