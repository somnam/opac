from typing import Any, Dict, List, Tuple

import tornado.web

from src.core.adapters import payload_to_catalog, payload_to_shelves
from src.core.entities import Book
from src.core.usecases import SearchLatestBooksUseCase
from src.dataproviders.repositories import DataRepository
from src.entrypoints.services import JobService
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin


class LatestBooksSearchHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
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

    def post(self, *args: Any, **kwargs: Any) -> None:

        with self.handle_error():
            payload = self.decode_message(self.request.body)

            use_case = SearchLatestBooksUseCase(DataRepository())

            result: List[Book] = use_case.execute(
                catalog=payload_to_catalog(payload["catalog"]),
                included_shelves=payload_to_shelves(payload["included_shelves"]),
                excluded_shelves=(payload["excluded_shelves"]),
            )

            self.write(self.encode_message({
                "items": [book.dict() for book in result],
            }))
