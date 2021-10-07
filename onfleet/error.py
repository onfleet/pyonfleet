class _OnfleetError(Exception):
    '''
    Base exception class for all errors raised by the Onfleet API.
    '''
    def __init__(self, message, status=None, request=None, cause=None):
        self.message = message
        self.status = status
        self.request = request
        self.cause = cause


class ValidationError(_OnfleetError):
    pass


class PermissionError(_OnfleetError):
    pass


class HttpError(_OnfleetError):
    pass


class RateLimitError(_OnfleetError):
    pass


class ServiceError(_OnfleetError):
    pass
