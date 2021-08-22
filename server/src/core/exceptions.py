class OpacException(Exception):
    pass


class DatabaseError(OpacException):
    pass


class ProfileNotFoundError(OpacException):
    pass
