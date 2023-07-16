from src.entrypoints.web.handlers.job_result import JobResultHandler
from src.entrypoints.web.handlers.latest_books import LatestBooksSearchHandler
from src.entrypoints.web.handlers.profile import ProfileHandler
from src.entrypoints.web.handlers.shelves import ShelvesHandler
from src.entrypoints.web.handlers.websocket import WebSocketHandler

__all__ = [
    "WebSocketHandler",
    "JobResultHandler",
    "ProfileHandler",
    "ShelvesHandler",
    "LatestBooksSearchHandler",
]
