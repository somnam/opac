from src.core.exceptions import BadRequest, NotFound


class MessageDecodeError(BadRequest):
    pass


class MessageSchemaError(BadRequest):
    pass


class MessageSchemaNotFound(NotFound):
    pass


class JobNotFound(NotFound):
    pass


class ClientNotFound(NotFound):
    pass


class OperationNotFound(NotFound):
    pass
