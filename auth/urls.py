from aiohttp import web

from .views import LoginView


urlpatterns = [
    web.route('*', '/api/v1/login', LoginView)
]
