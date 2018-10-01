from aiohttp import web
import aiohttp_autoreload

from core.db import db
from core import loaders
from settings import settings


async def init_app(*argv):
    """
    Initialize app
    :return:
    """

    middlewares = [

    ]

    app = web.Application(middlewares=middlewares)
    await db.set_bind(settings.DATABASE_URL)

    # Auto create tables
    await db.gino.create_all()

    app.router.add_routes(loaders.discover_urls())
    return app


if __name__ == '__main__':

    if settings.DEBUG:
        aiohttp_autoreload.start()

    web.run_app(init_app(), host=settings.APP_HOST, port=settings.APP_PORT)