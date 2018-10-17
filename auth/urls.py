from aiohttp import web

from .views import \
    LoginView, SignUpView, LogoutView, FacebookLoginView


urlpatterns = [
    web.view('/api/v1/login', LoginView),
    web.view('/api/v1/signup', SignUpView),
    web.view('/api/v1/logout', LogoutView),
    web.view('/api/v1/facebook_signup', FacebookLoginView)
]
