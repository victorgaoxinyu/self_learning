import sys
from pathlib import Path

import asyncpg
import asyncio
from play_with_connection_pool import product_query, query_product

sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed


@async_timed()
async def query_products_synchronously(pool, queries):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)

async def main():
    async with asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password',
        database='products',
        min_size=6,
        max_size=6
    ) as pool:
        
        await query_products_synchronously(pool, 10000)

        await query_products_concurrently(pool, 10000)
    
asyncio.run(main())
