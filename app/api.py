import json
import uvicorn
from starlette.responses import Response
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .routing import Router

class API:
    def __init__(self):
        self.routes = {}
        self.middleware = []

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
        if scope["type"] != "http":
            return
       
        path, kwargs = self.find_route(scope["path"])
        route = self.routes.get(path)

        if route is None:
            raise HTTPException(status_code=500)
        await route(scope, receive, send)

