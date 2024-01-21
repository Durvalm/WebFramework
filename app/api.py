import uvicorn
from starlette.responses import Response
from starlette.requests import Request

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

    def run(self, host='0.0.0.0', port=5200):
        print(f'Serving App on port {host}:{port}')
        uvicorn.run(self, host=host, port=port)

    # def as_asgi(self, scope):
    #     assert scope['type'] == 'http'

    #     async def asgi(receive, send):
    #         nonlocal scope
    #         request = Request(scope, receive)
    #         response = await self._dispatch(request)
    #         # await response(receive, send)
            
    #     return asgi


    # def __call__(self, scope):
    #     return self.as_asgi(scope)

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'


        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': b'oi',
        })
        return None

