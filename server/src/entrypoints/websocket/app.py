import argparse
import json
import logging
import logging.config
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import jsonschema
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from src.config import Config
from src.entrypoints.websocket.exceptions import MessageDecodeError
from src.entrypoints.websocket.handlers import (HandlerInterface,
                                                JobResultHandler,
                                                SearchLatestBooksHandler,
                                                SearchProfileHandler,
                                                PostProfileHandler,
                                                ShelvesHandler)

config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


class WebSocketApp(tornado.websocket.WebSocketHandler):
    handlers: List[Type[HandlerInterface]] = [
        SearchProfileHandler,
        PostProfileHandler,
        ShelvesHandler,
        SearchLatestBooksHandler,
    ]

    clients: Dict[str, Any] = dict()

    @property
    def handlers_map(self) -> Dict:
        if not hasattr(self, "_handlers_map"):
            self._handlers_map = {}

            for handler in self.handlers:
                self._handlers_map[handler.operation()] = handler()

        return self._handlers_map

    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/", cls, kwargs)

    def initialize(self) -> None:
        operations: List[str] = list(self.handlers_map.keys())

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
        logger.info("Open connection")

        if self.client_id not in WebSocketApp.clients:
            WebSocketApp.clients[self.client_id] = self

        self.write_message(json.dumps({
            "operation": 'open-connection',
            "payload": {"client_id": self.client_id},
        }))

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

        handler: Optional[HandlerInterface] = self.handlers_map.get(operation)

        if not handler:
            logger.error(f"Handler for operation {operation} not defined.")
            return

        handler.client_id = self.client_id

        response = await handler.execute(decoded_message["payload"])

        if response is not None:
            logger.info(f"Return message: {response}")

            self.write_message(json.dumps({"operation": operation, "payload": response}))

    def on_close(self) -> None:
        logger.info("Closing connection")
        if self.client_id in WebSocketApp.clients:
            del WebSocketApp.clients[self.client_id]

    def check_origin(self, origin: str) -> bool:
        logger.info(f"Origin: {origin}")
        return True


class JobResultApp(tornado.web.RequestHandler):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/client/(?P<client_id>\w+)/{0}".format(JobResultHandler.operation()), cls, kwargs)

    def post(self, *args: Any, **kwargs: Any) -> None:
        client_id = kwargs["client_id"]

        logger.info(f"Endpoint called with client_id {client_id}.")

        client = WebSocketApp.clients.get(client_id)

        if not client:
            logger.error(f"Client with id {client_id} not found.")
            return

        try:
            payload = json.loads(self.request.body)
        except json.JSONDecodeError as e:
            raise MessageDecodeError(str(e))

        response: Dict = JobResultHandler().execute(payload)

        client.write_message(json.dumps(response))


def run_app(port: int) -> None:

    app = tornado.web.Application(
        [
            WebSocketApp.route(),
            JobResultApp.route(),
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
        logger.info("Closing server.")


if __name__ == "__main__":
    run()
