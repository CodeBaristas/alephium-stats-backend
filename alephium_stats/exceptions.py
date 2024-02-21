from fastapi.responses import JSONResponse


################################################################################
# BASE EXCEPTIONS
class BaseError(Exception):  # pragma: no cover
    def __str__(self):
        return type(self).__name__


class MessageError(Exception):  # pragma: no cover
    def __str__(self):
        return self.message


################################################################################
# EXCEPTIONS
class UnauthorizedUseError(BaseError):
    pass


################################################################################
# HTTP ERRORS
# TEST: JSONResponse -> HTTPException + message
class BadRequestError(JSONResponse):  # pragma: no cover
    def __init__(self, detail):
        super().__init__({"detail": f"Bad Request: {detail}"}, status_code=400)


class UnauthorizedError(JSONResponse):  # pragma: no cover
    def __init__(self, detail):
        super().__init__({"detail": f"Unauthorized: {detail}"}, status_code=401)


class ForbiddenError(JSONResponse):  # pragma: no cover
    def __init__(self, detail):
        super().__init__({"detail": f"Forbidden: {detail}"}, status_code=403)


class NotFoundError(JSONResponse):  # pragma: no cover
    def __init__(self, detail):
        super().__init__({"detail": f"Unknown: {detail}"}, status_code=404)


class InternalError(JSONResponse):  # pragma: no cover
    def __init__(self, detail):
        super().__init__({"detail": f"Internal Error: {detail}"}, status_code=500)
