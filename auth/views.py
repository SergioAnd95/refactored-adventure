from aiohttp import web


class LoginView(web.View):
    async def get(self):
        return web.json_response({'text': 'Hello World'})