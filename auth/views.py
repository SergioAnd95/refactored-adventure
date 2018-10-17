from aiohttp import web
import secrets

from aiohttp_apispec import docs, use_kwargs
from passlib.hash import pbkdf2_sha256

import facebook

from .schema import RegistrationRequestSchema, LoginRequestSchema, FacebookLoginSchema
from .models import User
from .utils import set_get_token
from .decorators import login_required


class LoginView(web.View):
    @docs(
        tags=['Auth'],
        summary='Login endpoint',
        description='Login method'
    )
    @use_kwargs(LoginRequestSchema())
    async def post(self):
        data = self.request['data']
        user = await User.query.where(User.email == data['email']).gino.first()

        if not user or not user.password_match(data.get('password')):
            return web.json_response({'error': 'Invalid credentials'}, status=400)

        token = await set_get_token(self.request.app['redis'], user.id)

        return web.json_response({'token': token}, status=200)


class SignUpView(web.View):

    @docs(
        tags=['Auth'],
        summary='Signup endpoint',
        description='Signup method',
    )
    @use_kwargs(RegistrationRequestSchema())
    async def post(self):
        data = self.request['data']
        data['password'] = pbkdf2_sha256.hash(data['password'])

        await User.create(**data)

        return web.json_response({'msg': 'User created'}, status=201)


class FacebookLoginView(web.View):

    @docs(
        tags=['Auth'],
        summary='Facebook sign up endpoint',
        description='Facebook sign up method'
    )
    @use_kwargs(FacebookLoginSchema())
    async def post(self):
        data = self.request['data']
        access_token = data['token']
        try:
            graph = facebook.GraphAPI(access_token=access_token, version='3.0')
            user_info = graph.get_object('me', fields='id, name, email')
        except facebook.GraphAPIError:
            return web.json_response({'msg': 'Invlaid facebook user access token'}, status=500)

        user = await User.query.where(User.facebook_id == user_info['id']).gino.first()
        if not user:
            name = user_info['name'].split(' ')
            user = await User.create(
                email=user_info['email'],
                first_name=name[0],
                last_name=name[1],
                facebook_id=user_info['id']
            )

        token = await set_get_token(self.request.app['redis'], user.id)

        return web.json_response({'token': token})


@login_required
class LogoutView(web.View):

    @docs(
        tags=['Logout'],
        summary='Logout endpoint',
        description='Logout method',
        parameters=[{'in': "header", "name": "Authorization", "type": "string", "required": False,
                     "description": "User auth token"}]
    )
    async def post(self):
        if self.request.user:
            redis = self.request.app['redis']
            await redis.delete("user_token:%s" % self.request.token)
            return web.json_response({'msg': "User already logout"})

        return web.json_response({"msg": "User not login"}, status=401)
