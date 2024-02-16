import uvicorn
import re

from starlette.exceptions import HTTPException
from .middleware import ServerErrorMiddleware, ExceptionMiddleware, Middleware
from .routing import Route

class Api:
    def __init__(self, middleware):
        self.routes = {}
        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack = None

    def route(self, path):

        def wrapper(endpoint):
            route = Route(path=path, endpoint=endpoint)
            self.routes[path] = route
            return route

        return wrapper


    def find_route(self, url_path):
        for path, route in self.routes.items():
            kwargs = route.match(url_path)
            if kwargs is not None:
                return path, kwargs
        return None, {}


    def run(self, host='0.0.0.0', port=5200):
        print(f'Serving App on port {host}:{port}')
        uvicorn.run(self, host=host, port=port)


    async def __call__(self, scope, receive, send):
        if self.middleware_stack is None:
            self.middleware_stack = self.build_middleware_stack()
        await self.middleware_stack(scope, receive, send)

    
    async def app(self, scope, receive, send):
        path, kwargs = self.find_route(scope["path"])
        route = self.routes.get(path)

        if route is None:
            raise HTTPException(status_code=500)

        await route(scope, receive, send)


    def build_middleware_stack(self):
        middleware = (
            [Middleware(ServerErrorMiddleware)] 
            + self.user_middleware
            + [Middleware(ExceptionMiddleware)]
        )

        app = self.app
        for cls, args, kwargs in reversed(middleware):
            app = cls(app=app, *args, **kwargs)

        return app
    
    def mount(self, path, app, name):
        """calls Mount class, creates an ASGI app for staticfiles"""
        mount = Mount(path, app, name)
        self.routes[path] = mount
        return mount


class Mount:
    def __init__(self, path, app, name):
        self.path = path.rstrip("/")
        self.app = app
        self.name = name

    def match(self, url_path):
        result = re.match(r"^/static", url_path)
        return result

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    
