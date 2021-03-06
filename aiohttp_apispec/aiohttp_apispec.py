import copy
import warnings

from aiohttp import web
from aiohttp.hdrs import METH_ANY, METH_ALL
from apispec import APISpec, Path

from .utils import get_path, get_path_keys, issubclass_py37fix

PATHS = {'get', 'put', 'post', 'delete', 'patch'}


class AiohttpApiSpec:
    def __init__(
        self, url='/api/docs/api-docs', app=None, request_data_name='data', **kwargs
    ):
        warnings.warn(
            "'AiohttpApiSpec' will be removed since '1.0.0' version"
            " of 'aiohttp-apispec', use 'setup_aiohttp_apispec' instead",
            PendingDeprecationWarning,
        )
        self.spec = APISpec(**kwargs)
        if 'apispec.ext.marshmallow' not in self.spec.plugins:
            self.spec.setup_plugin('apispec.ext.marshmallow')
        self.url = url
        self._registered = False
        self._request_data_name = request_data_name
        if app is not None:
            self.register(app)

    def swagger_dict(self):
        return self.spec.to_dict()

    def register(self, app: web.Application):
        if self._registered is True:
            return None
        app['_apispec_request_data_name'] = self._request_data_name

        async def doc_routes(app_):
            self._register(app_)

        app.on_startup.append(doc_routes)
        self._registered = True

        def swagger_handler(request):
            return web.json_response(request.app['swagger_dict'])

        app.router.add_routes([web.get(self.url, swagger_handler)])

    def _register(self, app: web.Application):
        for route in app.router.routes():
            if issubclass_py37fix(route.handler, web.View) and route.method == METH_ANY:
                for attr in dir(route.handler):
                    if attr.upper() in METH_ALL:
                        view = getattr(route.handler, attr)
                        method = attr
                        self._register_route(route, method, view)
            else:
                method = route.method.lower()
                view = route.handler
                self._register_route(route, method, view)
        app['swagger_dict'] = self.swagger_dict()

    def _register_route(self, route: web.RouteDef, method, view):

        if not hasattr(view, '__apispec__'):
            return None

        url_path = get_path(route)
        if not url_path:
            return None

        view.__apispec__['parameters'].extend(
            {"in": "path", "name": path_key, "required": True, "type": "string"}
            for path_key in get_path_keys(url_path)
        )
        self._update_paths(view.__apispec__, method, url_path)

    def _update_paths(self, data: dict, method: str, url_path: str):
        operations = copy.deepcopy(data)

        if method in PATHS:
            self.spec.add_path(Path(path=url_path, operations={method: operations}))


def setup_aiohttp_apispec(
    app: web.Application,
    *,
    url: str = '/api/docs/api-docs',
    request_data_name: str = 'data',
    **kwargs
) -> None:
    """
    aiohttp-apispec extension.

    Usage:

    .. code-block:: python

        from aiohttp_apispec import docs, use_kwargs, setup_aiohttp_apispec
        from aiohttp import web
        from marshmallow import Schema, fields


        class RequestSchema(Schema):
            id = fields.Int()
            name = fields.Str(description='name')
            bool_field = fields.Bool()


        @docs(tags=['mytag'],
              summary='Test method summary',
              description='Test method description')
        @use_kwargs(RequestSchema)
        async def index(request):
            return web.json_response({'msg': 'done', 'data': {}})


        app = web.Application()
        app.router.add_post('/v1/test', index)

        # init docs with all parameters, usual for ApiSpec
        setup_aiohttp_apispec(app=app,
                              title='My Documentation',
                              version='v1',
                              url='/api/docs/api-docs')

        # now we can find it on 'http://localhost:8080/api/docs/api-docs'
        web.run_app(app)

    :param Application app: aiohttp web app
    :param str url: url for swagger spec in JSON format
    :param str request_data_name: name of the key in Request object
    where validated data will be placed by validation_middleware ('data' by default)
    :param kwargs: any apispec.APISpec kwargs
    """
    AiohttpApiSpec(url, app, request_data_name, **kwargs)
