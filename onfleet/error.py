class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

class PermissionError(Exception):
    def __init__(self, message, status, request):
        self.message = message
        self.status = status
        self.request = request

class HttpError(Exception):
    def __init__(self, message, status, request):
        self.message = message
        self.status = status
        self.request = request

class RateLimitError(Exception):
    def __init__(self, message, status, request):
        self.message = message
        self.status = status
        self.request = request

class ServiceError(Exception):
    def __init__(self, message, status, request):
        self.message = message
        self.status = status
        self.request = request