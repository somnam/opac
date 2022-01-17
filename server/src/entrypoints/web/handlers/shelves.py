from typing import Any, Dict, Tuple
from uuid import UUID

import tornado.web

from src.core.usecases import GetProfileShelvesUseCase
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin


class ShelvesHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile/(?P<profile_uuid>[^\/]+)/shelves", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "profile_uuid": {
                    "type": "string",
                    "format": "uuid",
                },
            },
            "required": ["profile_uuid"],
        }

    async def get(self, *args: Any, **kwargs: Any) -> None:
        with self.handle_error():
            self.validate_message(kwargs)

            use_case = GetProfileShelvesUseCase(DataRepository())

            shelves = await use_case.execute(UUID(kwargs["profile_uuid"]))

            self.write(self.encode_message({
                "items": [shelf.dict() for shelf in shelves],
            }))
