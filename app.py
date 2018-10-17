import asyncio

from aiohttp import web

import uvloop

import aioredis
import aiohttp_autoreload
from aiohttp_swagger import *
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from core.db import db
from core import loaders, middlewares as core_middlewares
from auth import middlewares as auth_middlewares
from settings import settings


async def swagger(app):
    setup_swagger(
        app=app, swagger_url='/api/v1/doc', swagger_info=app['swagger_dict']
    )


async def init_app(*argv):
    """
    Initialize app
    :return:
    """
    redis_pool = await aioredis.create_redis_pool('redis://localhost/0')


    middlewares = [
        core_middlewares.validation_error_middleware,
        auth_middlewares.auth_middleware,
        validation_middleware,
    ]

    app = web.Application(middlewares=middlewares)
    app['redis'] = redis_pool
    await db.set_bind(settings.DATABASE_URL)

    # Auto create tables
    await db.gino.create_all()

    app.router.add_routes(loaders.discover_urls())
    setup_aiohttp_apispec(app=app,
                          title='Refactored Adventure',
                          version='v1',
                          url='/api/docs/api-docs')
    app.on_startup.append(swagger)
    return app


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    if settings.DEBUG:
        aiohttp_autoreload.start()

    web.run_app(init_app(), host=settings.APP_HOST, port=settings.APP_PORT)