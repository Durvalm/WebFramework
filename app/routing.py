from parse import parse
import json

from starlette.responses import Response

class Router:
    def __init__(self, path, endpoint):
        self.path = path
        self.endpoint = endpoint
 

    def match(self, url_path):
        """Returns kwargs in url path"""
        result = parse(self.path, url_path)
        if result is not None:
            return result.named
        return None
    

    async def __call__(self, scope, receive, send):
        kwargs = self.match(scope["path"])
        response = get_response_from_endpoint(self.endpoint, kwargs)
        await response(scope, receive, send)


def get_response_from_endpoint(endpoint, kwargs):
    """Helper function to call endpoint, and return jsonized data as a response"""
    if kwargs is not None:
        response_obj = endpoint(**kwargs)
    else:
        response_obj = endpoint()

    json_data = json.dumps({'data': response_obj})
    response = Response(json_data, media_type='application/json')
    return response


