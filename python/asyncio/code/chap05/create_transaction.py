import asyncio
import asyncpg
import logging

async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')"
                                 )
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')"
                                 )
        
        query = """SELECT brand_name FROM brand
                    WHERE brand_name LIKE 'brand%'"""
        
        brands = await connection.fetch(query)
        print("*" * 10)
        print(brands)

        await connection.close()


async def handle_exception_in_transaction():
    async def query_big_brand(c):
        print(">" * 10)
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)
        print(f"Query result was: {brands}")
        return 

    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )

    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await query_big_brand(connection)  # at this moment insert should be done
            await connection.execute(insert_brand)  # this should raise exception
    except Exception:
        logging.exception('Error while running transaction')
    finally:
        await query_big_brand(connection)  # insert should be reverted
                                           # as transaction got rolled back due to exception
        await connection.close()


async def handle_exception_with_nested_transaction():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")  # success
        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")  # failed and rolled back
        except Exception as ex:
            logging.warning("Ignoring error inserting product color", exc_info=ex)
    
    await connection.close()


async def manually_manage_transaction():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )

    transaction = connection.transaction() # init instance
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Errors, rolling back transaction!')
        await transaction.rollback()
    else:
        print("No errors, committing the transaction!")
        await transaction.commit()
    
    print(">" * 10)
    query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(f"Query result was: {brands}")

    await connection.close()

# asyncio.run(main())
# asyncio.run(handle_exception_in_transaction())
# asyncio.run(handle_exception_with_nested_transaction())    
asyncio.run(manually_manage_transaction())