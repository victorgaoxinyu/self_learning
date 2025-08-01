import functools
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg_connection_util import DB_KEY, create_database_pool, destroy_database_pool


routes = web.RouteTableDef()

@routes.get('/users/{id}/favourites')
async def favourites(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        user_id = int(str_id)
        db = request.app[DB_KEY]
        favourite_query = 'SELECT product_id from user_favourite where user_id = $1'
        result = await db.fetch(favourite_query, user_id)
        if result is not None:
            return web.json_response(
                [
                    dict(record) for record in result
                ]
            )
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()


app = web.Application()
app.on_startup.append(functools.partial(
    create_database_pool,
    host='127.0.0.1',
    port=5432,
    user='postgres',
    password='password',
    database='favourites'
))

app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)

web.run_app(app, port=8002)