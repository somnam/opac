import logging
from typing import Any, Dict, Tuple

import tornado.web
from src.core.adapters import payload_to_profile
from src.core.usecases import PostProfileUseCase
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.exceptions import MessageDecodeError
from src.entrypoints.web.mixin import JsonSchemaMixin

logger = logging.getLogger(__name__)


class ProfileHandler(tornado.web.RequestHandler, JsonSchemaMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/profile", cls, kwargs)

    def initialize(self) -> None:
        self.message_schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1
                },
                "value": {
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": ["name", "value"],
        }

        self.use_case = PostProfileUseCase(DataRepository())

    def post(self, *args: Any, **kwargs: Any) -> None:

        try:
            payload = self.decode_message(self.request.body)
        except MessageDecodeError as e:
            logger.error(f"Error decoding message: {e!s}")
            return

        self.use_case.execute(payload_to_profile(payload))
