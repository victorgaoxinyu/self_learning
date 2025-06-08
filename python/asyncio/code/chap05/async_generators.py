import sys
from pathlib import Path
from types import TracebackType
from typing import Optional, Type
import asyncpg
import asyncio

sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed, delay


class ConnectedPostgres:
    def __init__(self):
        self._connection = None

    async def __aenter__(self):
        print("Enter async context manager, create connection to pg")
        self._connection = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            database='products',
            password='password',
        )
        return self._connection

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]):
        print("Existing context manager, close connection with pg")
        await self._connection.close()

async def positive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer
    
@async_timed()
async def main():
    async_generator = positive_integers_async(3)
    print(type(async_generator))  # async_generator
    async for number in async_generator:  # for loop for async_generator
        print(f"Got {number}")


async def stream_single_element_a_time():
    async with ConnectedPostgres() as connection:
        query = 'SELECT product_id, product_name FROM product'
        async with connection.transaction():
            async for product in connection.cursor(query):
                print(product)


async def move_cursor_and_fetch():
    async with ConnectedPostgres() as connection:
        query = 'SELECT product_id, product_name FROM product'
        async with connection.transaction():
            cursor = await connection.cursor(query)
            await cursor.forward(500)
            products = await cursor.fetch(100)  # this impl does not contain generator
            for product in products:
                print(product)


async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count = item_count + 1
        yield item


async def async_generator():
    async with ConnectedPostgres() as connection:
        async with connection.transaction():
            query = 'SELECT product_id, product_name FROM product'
            product_generator = connection.cursor(query)
            async for product in take(product_generator, 5):
                print(product)


# asyncio.run(main())
# asyncio.run(stream_single_element_a_time())
# asyncio.run(move_cursor_and_fetch())
asyncio.run(async_generator())