import logging
from typing import Any, Dict, List, Tuple, Type, Union

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

from src.entrypoints.exceptions import OperationNotFound
from src.entrypoints.web.handlers.websocket.base import IWebSocketOperation
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin

logger = logging.getLogger(__name__)


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonSchemaMixin, ErrorHandlerMixin):
    operations: List[Type[IWebSocketOperation]] = []

    @property
    def operations_map(self) -> Dict:
        if not hasattr(self, "_operations_map"):
            self._operations_map = {}

            for operation in self.operations:
                self._operations_map[operation.name()] = operation()

        return self._operations_map

    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/ws", cls, kwargs)

    def initialize(self) -> None:
        operations: List[str] = list(self.operations_map.keys())

        # Set message schema.
        self.message_schema = {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": operations,
                },
                "payload": {"type": ["object", "null"]},
            },
            "required": ["operation", "payload"],
        }

        # Don't close WS connections after 60s.
        self.settings["websocket_ping_interval"] = 30

        self.client_id = str(hash(self))

    def open(self, *args: str, **kwargs: str) -> None:
        """Client opens a websocket connection."""
        logger.info(f"Open connection for client {self.client_id}")

    async def on_message(self, message: Union[str, bytes]) -> None:
        logger.info(f"Got message: {message!r}")

        with self.handle_error():
            decoded_message = self.decode_message(message)

            operation_name = decoded_message["operation"]

            operation = self.operations_map.get(operation_name)

            if not operation:
                raise OperationNotFound(f"Operation {operation_name} not defined.")

            operation.client_id = self.client_id

            response = await operation.execute(decoded_message["payload"])

            if response is not None:
                logger.info(f"Return message: {response}")

                self.write_message(
                    self.encode_message(
                        {
                            "operation": operation_name,
                            "payload": response,
                        }
                    )
                )

    def on_close(self) -> None:
        logger.info(f"Closing connection for client {self.client_id}")

    def check_origin(self, origin: str) -> bool:
        logger.info(f"Origin: {origin}")
        return True
