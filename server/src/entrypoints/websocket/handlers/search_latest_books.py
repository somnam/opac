import asyncio
import logging
import re
from typing import List

from src.core.entities import Catalog, Shelf, Profile
from src.dataproviders.repositories import DataRepository
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.entrypoints.jobs import search_latest_books, on_result

logger = logging.getLogger('src.entrypoints.websocket')


class SearchLatestBooksHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-latest-books'

    async def execute(self, payload: dict) -> None:
        await asyncio.sleep(0)

        catalog = self._payload_to_catalog(payload["catalog"])

        included_shelves = self._payload_to_shelves(payload["included_shelves"])

        excluded_shelves = self._payload_to_shelves(payload["excluded_shelves"])

        DataRepository().job.enqueue(
            search_latest_books,
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
            on_success=on_result,
        )

    def _payload_to_catalog(self, payload: dict) -> Catalog:

        result = re.search(r'^([^\(]+)\s\(([^\)]+)\)$', payload["name"])

        if result:
            name, city = result.groups()
        else:
            name, city = "", ""

        return Catalog(name=name, city=city, value=payload["value"])

    def _payload_to_shelves(self, payload: list) -> List[Shelf]:
        return [
            Shelf(
                name=item["name"],
                value=item["value"],
                profile=Profile(**item["profile"]),
                pages=item["pages"],
            )
            for item in payload
        ]
