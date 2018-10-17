from aiohttp import web
from json.decoder import JSONDecodeError


@web.middleware
async def validation_error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPClientError as e:
        e.set_status(status=400)
        return e
    except JSONDecodeError:
        return web.json_response({'msg': 'JSON decode error'}, status=500)
