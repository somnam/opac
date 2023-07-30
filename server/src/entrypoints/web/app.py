import argparse
import logging
import logging.config

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

from src.config import Config
from src.entrypoints.web.handlers.job_result import JobResultHandler
from src.entrypoints.web.handlers.latest_books import LatestBooksSearchHandler
from src.entrypoints.web.handlers.profile import ProfileHandler, ProfileSearchHandler
from src.entrypoints.web.handlers.shelves import ShelvesHandler, ShelvesSearchHandler
from src.entrypoints.web.handlers.websocket import WebSocketHandler

config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


def run_app(port: int) -> None:
    app = tornado.web.Application(
        [
            WebSocketHandler.route(),
            JobResultHandler.route(),
            ProfileHandler.route(),
            ProfileSearchHandler.route(),
            ShelvesHandler.route(),
            ShelvesSearchHandler.route(),
            LatestBooksSearchHandler.route(),
        ],
    )

    # Setup server.
    tornado.httpserver.HTTPServer(app).listen(port)

    # Start event loop.
    tornado.ioloop.IOLoop.current().start()


def parse_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(description="Tornado app.")

    args_parser.add_argument("-p", "--port", type=int, default=8888, help="Server port")

    args = args_parser.parse_args()

    return args


def run() -> None:
    args = parse_args()

    logger.info(f"Starting server on port={args.port}")

    try:
        run_app(args.port)
    except KeyboardInterrupt:
        logger.info("Closing server.")


if __name__ == "__main__":
    run()
