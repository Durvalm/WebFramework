from parse import parse

class Route:
    def __init__(self, handler, pattern):
        self._handler = handler
        self._pattern = pattern

    def match(self, path):
        """Returns kwargs in url path"""
        result = parse(self._pattern, path)
        if result is not None:
            return result.named
        return None
    

