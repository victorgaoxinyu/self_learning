import asyncpg
import asyncio
from db_product_schema import *
from asyncpg import Record

async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='postgres',
        password='password',
    )

    version = connection.get_server_version()
    print(f'Connected! Postgres version is {version}')

    await connection.close()


async def use_execute_coroutine_to_create_tables():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_SKU_TABLE,
        SIZE_INSERT,
        COLOR_INSERT,
    ]

    print("Creating the product database")
    for statement in statements:
        status = await connection.execute(statement)  # execute() is a coroutine, need await
        print(status)
    await connection.close()


async def insert_brand_data_and_validate():
    connection = await asyncpg.connect(  # create context manager?
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    brand_query = 'SELECT brand_id, brand_name FROM brand'

    results = await connection.fetch(brand_query)

    for brand in results:
        print(f'id: {brand["brand_id"]}, name: {brand["brand_name"]}')

    await connection.close()

# asyncio.run(main())
# asyncio.run(use_execute_coroutine_to_create_tables())
asyncio.run(insert_brand_data_and_validate())