from typing import Optional


class OpacException(Exception):
    def __init__(self, message: str, detail: str, code: int, *args: object) -> None:
        self.message = message
        self.detail = detail
        self.code = code

        super().__init__(*args)


class BadRequest(OpacException):
    message = "Bad Request"
    detail = "The server could not understand the request due to invalid syntax."

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(message=self.message, detail=(detail or self.detail), code=400)


class NotFound(OpacException):
    message = "Not Found"
    detail = "The server can not find the requested resource."

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(message=self.message, detail=(detail or self.detail), code=404)


class InternalServerError(OpacException):
    message = "Internal Server Error"
    detail = "The server has encountered a situation it does not know how to handle."

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(message=self.message, detail=(detail or self.detail), code=500)


class BadGateway(OpacException):
    message = "Bad Gateway"
    detail = (
        "The server, while working as a gateway to handle the request, got an invalid response."
    )

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(message=self.message, detail=(detail or self.detail), code=502)


class DatabaseError(InternalServerError):
    pass


class ProfileNotFoundError(NotFound):
    pass
