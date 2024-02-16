import re
import os
from starlette.responses import FileResponse

class StaticFiles:
    
    def __init__(self, directory):
        self.directory = directory
    
    async def __call__(self, scope, receive, send):
        """ASGI entry point"""
        assert scope["type"] == "http"
        path = self.get_path(scope)
        response = await self.get_file_response(path)
        await response(scope, receive, send)
    
    def get_path(self, scope):
        """return the string path"""
        root_path = "/"+self.directory
        route_path = re.sub(r"^" + root_path, "", scope["path"])
        return os.path.normpath(os.path.join(*route_path.split("/")))
    
    async def get_file_response(self, path):
        """Returns file response (should use FileResponse class from starlette)"""
        full_path = self.lookup_path(path)
        response = FileResponse(full_path)

        return response
    
    def lookup_path(self, path):
        joined_path = os.path.join(self.directory, path)
        full_path = os.path.realpath(joined_path)
        return full_path
    
