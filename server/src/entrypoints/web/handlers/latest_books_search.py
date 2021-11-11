import logging
from typing import Any, Dict, List, Tuple

import tornado.web

from src.core.entities import Book
from src.core.adapters import payload_to_catalog, payload_to_shelves
from src.core.usecases import SearchLatestBooksUseCase
from src.dataproviders.repositories import DataRepository
from src.entrypoints.exceptions import MessageDecodeError
from src.entrypoints.services import JobService
from src.entrypoints.web.mixin import JsonSchemaMixin

logger = logging.getLogger(__name__)


class LatestBooksSearchHandler(tornado.web.RequestHandler, JsonSchemaMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/latest-books/search", cls, kwargs)

    def initialize(self) -> None:
        self.job_service = JobService()

        shelf_schema = {
            "type": "object",
            "properties": {

            },
        }

        self.message_schema = {
            "type": "object",
            "properties": {
                "catalog": {
                    "type": "object",
                    "properties": {

                    }
                },
                "included_shelves": {
                    "type": "array",
                    "items": shelf_schema,
                },
                "excluded_shelves": {
                    "type": "array",
                    "items:": shelf_schema,
                },
            },
            "required": [
                "catalog",
                "included_shelves",
                "excluded_shelves",
            ],
        }

        self.use_case = SearchLatestBooksUseCase(DataRepository())

    def post(self, *args: Any, **kwargs: Any) -> None:

        try:
            payload = self.decode_message(self.request.body)
        except MessageDecodeError as e:
            logger.error(f"Error decoding message: {e!s}")
            return

        result: List[Book] = self.use_case.execute(
            catalog=payload_to_catalog(payload["catalog"]),
            included_shelves=payload_to_shelves(payload["included_shelves"]),
            excluded_shelves=(payload["excluded_shelves"]),
        )

        self.write({"items": [book.to_dict() for book in result]})
