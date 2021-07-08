import asyncio
import logging
import re

from src.core.entities import Catalog, Profile
from src.dataproviders.repositories import DataRepository
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.entrypoints.jobs import search_latest_books, job_on_success

logger = logging.getLogger('src.entrypoints.websocket')


class SearchLatestBooksHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-latest-books'

    async def execute(self, payload: dict) -> None:
        await asyncio.sleep(0)

        catalog = self._payload_to_catalog(payload)

        profile = self._payload_to_profile(payload)

        repository = DataRepository()

        repository.job.enqueue(
            search_latest_books,
            meta={"operation": "search-latest-books", "progress": 0, "client_id": self.client_id},
            kwargs={
                "catalog": catalog.to_dict(),
                "profile": profile.to_dict(),
            },
            on_success=job_on_success,
        )

    def _payload_to_catalog(self, payload: dict) -> Catalog:

        result = re.search(r'^([^\(]+)\s\(([^\)]+)\)$', payload["catalog"]["name"])

        if result:
            name, city = result.groups()
        else:
            name, city = "", ""

        return Catalog(name=name, city=city, value=payload["catalog"]["value"])

    def _payload_to_profile(self, payload: dict) -> Profile:
        return Profile(**payload["profile"])
