import argparse
import json
import logging
from typing import Any, Dict, Optional, Sequence, Tuple, Type, Union

import jsonschema
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from src.entrypoints.websocket.exceptions import MessageDecodeError
from src.entrypoints.websocket.handlers import (ActivitiesHandler,
                                                CatalogsHandler,
                                                HandlerInterface,
                                                SearchProfileHandler,
                                                ShelvesHandler)

logger = logging.getLogger("server")


class WebSocketApp(tornado.websocket.WebSocketHandler):
    handlers: Dict[str, Type[HandlerInterface]] = {}

    @classmethod
    def register_handlers(cls, handlers: Sequence[Type[HandlerInterface]]) -> None:
        for handler in handlers:
            cls.handlers[handler.operation()] = handler

    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/", cls, kwargs)

    def initialize(self) -> None:
        # Set message schema.
        self.message_schema = {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": list(self.handlers.keys()),
                },
                "payload": {"type": ["object", "null"]},
            },
            "required": ["operation", "payload"],
        }

        # Don't close WS connections after 60s.
        self.settings["websocket_ping_interval"] = 30

    def open(self, *args: str, **kwargs: str) -> None:
        """Client opens a websocket connection."""
        logger.info("Open connection")

    async def on_message(self, message: Union[str, bytes]) -> None:
        logger.info(f"Got message: {message!r}")

        try:
            decoded_message = self._decode_message(message)
        except MessageDecodeError as e:
            logging.error(f"Error decoding message: {e!s}")
            return

        await self._handle_message(decoded_message)

    def _decode_message(self, message: Union[str, bytes]) -> Dict:
        try:
            decoded_message: Dict = json.loads(message)
            jsonschema.validate(
                instance=decoded_message,
                schema=self.message_schema,
            )
        except (
            json.JSONDecodeError,
            jsonschema.exceptions.SchemaError,
            jsonschema.exceptions.ValidationError,
        ) as e:
            raise MessageDecodeError(str(e))

        return decoded_message

    async def _handle_message(self, decoded_message: Dict) -> None:
        operation = decoded_message["operation"]

        handler_class: Optional[Type[HandlerInterface]] = self.handlers.get(operation)

        if not handler_class:
            logger.error(f"Handler for operation {operation} not defined")
            return

        handler = handler_class()

        response = await handler.execute(decoded_message["payload"])

        logger.info(f"Return message: {response}")

        self.write_message(json.dumps({"operation": operation, "payload": response}))

    def on_close(self) -> None:
        logger.info("Closing connection")

    def check_origin(self, origin: str) -> bool:
        logger.info(f"Origin: {origin}")
        return True


def run_app(port: int) -> None:
    WebSocketApp.register_handlers((
        SearchProfileHandler,
        ShelvesHandler,
        CatalogsHandler,
        ActivitiesHandler,
    ))

    app = tornado.web.Application(
        [
            WebSocketApp.route(),
        ],
    )

    # Setup server.
    tornado.httpserver.HTTPServer(app).listen(port)

    # Start event loop.
    logger.info(f"Starting server on port={port}")
    tornado.ioloop.IOLoop.instance().start()


def parse_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(description="Test ws server")

    args_parser.add_argument("-p", "--port", type=int, default=8888,
                             help="Server port")

    args_parser.add_argument("-d", "--debug", action="store_true",
                             help="Debug mode")

    args = args_parser.parse_args()

    return args


def run() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    try:
        run_app(args.port)
    except KeyboardInterrupt:
        logger.info("Closing src.")


if __name__ == "__main__":
    run()
