

class ASGIMiddleware():
    """Base class for ASGI middleware classes"""

    def __init__(self, inner, app, **kwargs):
        self.inner = inner
        self.app = app
        self.kwargs = kwargs

    def __call__(self, scope):
        return self.inner(scope)