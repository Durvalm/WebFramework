import uvicorn
from starlette.responses import Response
from starlette.requests import Request
from starlette.exceptions import HTTPException

from .routing import Route

class API:

    def __init__(self):
        self._routes = {}

    def route(self, pattern):

        def wrapper(handler):
            route = Route(pattern=pattern, handler=handler)
            self._routes[pattern] = route
            return route

        return wrapper

    def _find_route(self, path):
        for pattern, route in self._routes.items():
            kwargs = route.match(path)
            if kwargs is not None:
                return pattern, kwargs
        return None, {}

    def run(self, host='0.0.0.0', port=5200):
        print(f'Serving App on port {host}:{port}')
        uvicorn.run(self, host=host, port=port)

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        request = Request(scope, receive)

        pattern, kwargs = self._find_route(request.url.path)
        route = self._routes.get(pattern)
        if route is None:
            raise HTTPException

        response_obj = route._handler()
        response = Response(response_obj, media_type='text/plain')
        await response(scope, receive, send)

        return response_obj

