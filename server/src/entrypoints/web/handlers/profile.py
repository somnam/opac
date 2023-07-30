import logging
from typing import Any, Dict, Tuple

import tornado.web

from src.core.transforms import payload_to_profile, payload_to_profile_search_params
from src.core.usecases.create_profile import CreateProfileUseCase
from src.core.usecases.search_profile import SearchProfileUseCase
from src.dataproviders.gateways.data import DataGateway
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin

logger = logging.getLogger(__name__)


class ProfileHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "value": {"type": "string", "minLength": 1},
            },
            "required": ["name", "value"],
        }

    async def post(self, *args: Any, **kwargs: Any) -> None:
        with self.handle_error():
            payload = self.decode_message(self.request.body)

            use_case = CreateProfileUseCase(repository=DataRepository())
            await use_case.execute(payload_to_profile(payload))


class ProfileSearchHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile/search", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "phrase": {"type": "string", "minLength": 1},
                "page": {"type": "integer", "minimum": 1},
            },
            "required": ["phrase"],
        }

    async def post(self, *args: Any, **kwargs: Any) -> None:
        with self.handle_error():
            payload = self.decode_message(self.request.body)

            use_case = SearchProfileUseCase(gateway=DataGateway())
            result = await use_case.execute(payload_to_profile_search_params(payload))

            self.write(self.encode_message(result.dict()))
            self.set_header("Content-Type", "application/json")
