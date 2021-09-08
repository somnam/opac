import asyncio
import logging

from src.core.adapters import payload_to_catalog, payload_to_shelves
from src.entrypoints.services import JobService
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.entrypoints.tasks import search_latest_books

logger = logging.getLogger(__name__)


class SearchLatestBooksHandler(HandlerInterface):
    def __init__(self) -> None:
        self._job_service = JobService()

    @classmethod
    def operation(cls) -> str:
        return 'search-latest-books'

    async def execute(self, payload: dict) -> None:
        catalog = payload_to_catalog(payload["catalog"])

        included_shelves = payload_to_shelves(payload["included_shelves"])

        excluded_shelves = payload_to_shelves(payload["excluded_shelves"])

        self._job_service.enqueue(
            job=search_latest_books,
            meta={
                "operation": "search-latest-books",
                "progress": 0,
                "client_id": self.client_id
            },
            kwargs={
                "catalog": catalog.to_dict(),
                "included_shelves": [shelf.to_dict() for shelf in included_shelves],
                "excluded_shelves": [shelf.to_dict() for shelf in excluded_shelves],
            },
            on_success=self._job_service.push_result,
        )

        await asyncio.sleep(0)
