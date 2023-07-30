import logging
from typing import Any, Dict, Tuple
from uuid import UUID

import tornado.web

from src.core.transforms import payload_to_shelf_search_params
from src.core.usecases.get_profile import GetProfileUseCase
from src.core.usecases.get_shelves import GetProfileShelvesUseCase
from src.core.usecases.search_shelves import SearchShelvesUseCase
from src.dataproviders.gateways.data import DataGateway
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin

logger = logging.getLogger(__name__)


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
            self.set_header("Content-Type", "application/json")


class ShelvesSearchHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile/(?P<profile_uuid>[^\/]+)/shelves/search", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "phrase": {"type": "string", "minLength": 1},
                "page": {"type": "integer", "minimum": 1},
            },
            "required": [],
        }

    async def post(self, *args: Any, **kwargs: Any) -> None:
        with self.handle_error():
            payload = kwargs | self.decode_message(self.request.body)

            use_case = SearchShelvesUseCase(repository=DataRepository(), gateway=DataGateway())
            search_results = await use_case.execute(payload_to_shelf_search_params(payload))

            self.write(self.encode_message(search_results.dict()))
            self.set_header("Content-Type", "application/json")
