from typing import Any, Dict, Tuple

import tornado.web

from src.core.usecases import GetProfileShelvesUseCase
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin


class ShelvesHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile/(?P<profile_id>\w+)/shelves", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "profile_id": {
                    "type": "string",
                    "minLength": 32,
                    "maxLength": 32,
                },
            },
            "required": ["profile_id"],
        }

    def get(self, *args: Any, **kwargs: Any) -> None:
        with self.handle_error():
            self.validate_message(kwargs)

            use_case = GetProfileShelvesUseCase(DataRepository())

            shelves = use_case.execute(kwargs["profile_id"])

            self.write(self.encode_message({
                "items": [shelf.to_dict() for shelf in shelves],
            }))
