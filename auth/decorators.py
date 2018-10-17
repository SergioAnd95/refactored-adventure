from aiohttp import web


def login_required(f):
    """
    Decorator for allow access
    only for login user
    """

    async def wrapped(request, *args):
        if request.user:
            return await f(request, *args)
        return web.json_response({'msg': 'User not login'}, status=401)
    return wrapped