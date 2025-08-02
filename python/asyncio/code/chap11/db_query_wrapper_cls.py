# 不能同时运行多个查询
# 尝试运行查询之前，数据库连接可能没有初始化
# 如果想运行查询，只有正确初始化连接后才可以

import asyncio
from enum import Enum

class ConnectionState(Enum):
    WAIT_INIT = 0
    INITIALISING = 1
    INITIALISED = 2


class Connection:

    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = asyncio.Condition()

    async def initialise(self):
        await self._change_state(ConnectionState.INITIALISING)
        print('initialise: Initialising connection...')
        await asyncio.sleep(3)
        print('initialise: Finished initialising connection')
        await self._change_state(ConnectionState.INITIALISED)

    async def execute(self, query: str):
        async with self._condition:
            print('execute: Waiting for connection to initialise')
            await self._condition.wait_for(self._is_initialised)
            print(f'execute: Running {query}')
            await asyncio.sleep(3)

    def _is_initialised(self):
        if self._state is not ConnectionState.INITIALISED:
            print(f'_is_initialised: Connection not finished initialising... state is {self._state}')
            return False
        else:
            print(f'_is_initialised: Connection is initialised')
            return True

    async def _change_state(self, state: ConnectionState):
        async with self._condition:
            print(f"change_state: State changing from {self._state} to {state}")
            self._state = state
            self._condition.notify_all()


async def main():
    connection = Connection()
    query_one = asyncio.create_task(connection.execute('select * from table'))
    query_two = asyncio.create_task(connection.execute('select * from other_table'))
    asyncio.create_task(connection.initialise())
    await query_one
    await query_two


asyncio.run(main())