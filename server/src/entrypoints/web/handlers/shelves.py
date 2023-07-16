from typing import Any, Dict, Tuple
from uuid import UUID

import tornado.web

from src.core.usecases import GetProfileShelvesUseCase, GetProfileUseCase
from src.dataproviders.gateways import DataGateway
from src.dataproviders.repositories import DataRepository
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

            profile_use_case = GetProfileUseCase(repository=DataRepository())
            profile = await profile_use_case.execute(UUID(kwargs["profile_uuid"]))

            shelves_use_case = GetProfileShelvesUseCase(
                repository=DataRepository(),
                gateway=DataGateway(),
            )
            shelves = await shelves_use_case.execute(profile)

            self.write(
                self.encode_message(
                    {
                        "items": [shelf.dict() for shelf in shelves],
                    }
                )
            )
