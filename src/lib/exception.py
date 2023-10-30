
class BaseException(Exception):

    def __init__(self, msg="", *args: object) -> None:
        super().__init__(*args)
        self.msg = msg
        self.status = 400
        self.errors = {}


class BadRequest(BaseException):
    def __init__(self, msg="Bad request", errors={}, *args: object) -> None:
        super().__init__(msg, *args)
        self.errors = errors


class Forbidden(BaseException):
    def __init__(self, msg="Forbidden", errors={}, *args: object) -> None:
        super().__init__(msg, *args)
        self.errors = errors
        self.status = 403


class NotFound(BaseException):
    def __init__(self, msg="NotFound", errors={}, *args: object) -> None:
        super().__init__(msg, *args)
        self.error = errors
        self.status = 404


class MethodNotAllow(BaseException):
    def __init__(self, msg="Method not allow", *args: object) -> None:
        super().__init__(msg, *args)
        self.status = 405


class ConflictError(BaseException):
    def __init__(self, msg="Conflict", *args: object) -> None:
        super().__init__(msg, *args)
        self.status = 409


class InternalServer(BaseException):
    def __init__(self, msg="Internal server error", errors={}, *args: object) -> None:
        super().__init__(msg, *args)
        self.errors = errors
        self.status = 500
