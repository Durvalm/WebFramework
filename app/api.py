import uvicorn

from starlette.exceptions import HTTPException
from .middleware import ServerErrorMiddleware, ExceptionMiddleware, Middleware
from .routing import Router

class API:
    def __init__(self, middleware):
        self.routes = {}
        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack = None

    def route(self, path):

        def wrapper(endpoint):
            route = Router(path=path, endpoint=endpoint)
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

