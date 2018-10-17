import re

from aiohttp import web

from auth.models import User


@web.middleware
async def auth_middleware(request, handler) -> web.Response:
    request.user = None
    request.token = None
    if 'Authorization' in request.headers:
        try:
            scheme, token = request.headers.get(
                'Authorization'
            ).strip().split(' ')
        except ValueError:
            raise web.HTTPForbidden(
                reason='Invalid authorization header',
            )

        if not re.match('Bearer', scheme):
            raise web.HTTPForbidden(
                reason='Invalid token scheme',
            )
        redis = request.app['redis']
        user_id = await redis.get("user_token:%s" % token)

        if not user_id:
            raise web.HTTPForbidden(
                reason='Invalid token',
            )
        user = await User.get(int(user_id))
        if not user:
            raise web.HTTPForbidden(
                reason='User with this token doesn\'t exist',
            )
        request.user = user
        request.token = token

    resp = await handler(request)
    return resp