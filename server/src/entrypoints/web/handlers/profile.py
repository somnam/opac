from typing import Any, Dict, Tuple

import tornado.web

from src.core.transforms import payload_to_profile
from src.core.usecases import CreateProfileUseCase
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin


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
