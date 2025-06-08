import asyncpg
import asyncio
from db_product_schema import *
from asyncpg import Record
from random import sample, randint


def load_common_words():
    with open("common_words.txt") as common_words:
        return common_words.readlines()


def generate_brand_names(words):
    return [(words[index],) for index in sample(range(100), 100)]


def generate_products(common_words, brand_id_start, brand_id_end, products_to_create):
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(1000), 10)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))

    return products


def generate_skus(product_id_start, product_id_end, skus_to_create):
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))

    return skus


async def insert_brands(common_words, connection):
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


# insert brands
async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        database="products",
        password="password",
    )

    await insert_brands(common_words, connection)


# insert products and skus
async def insert_products_and_skus():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        database="products",
        password="password",
    )

    product_tuples = generate_products(
        common_words,
        brand_id_start=1,
        brand_id_end=100,
        products_to_create=1000,
    )

    await connection.executemany(
        "INSERT INTO product VALUES(DEFAULT, $1, $2)", product_tuples
    )
    sku_tuples = generate_skus(
        product_id_start=1,
        product_id_end=1000,
        skus_to_create=100000
    )

    await connection.executemany(
        "INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)", sku_tuples
    )

    await connection.close()

# asyncio.run(main())
asyncio.run(insert_products_and_skus())