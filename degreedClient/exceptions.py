class PathgatherApiException(Exception):
    def __init__(self, message, uri=None):
        self.message = message
        self.uri = uri
        if self.uri:
            self.message += "({0})".format(uri)


class UserNotFoundException(PathgatherApiException):
    pass
