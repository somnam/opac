import datetime
import json
import logging
from abc import abstractmethod
from contextlib import contextmanager
from json import JSONEncoder
from typing import Any, Dict, Generator, Optional, Union
from uuid import UUID

import jsonschema

from src.core.exceptions import OpacException
from src.entrypoints.exceptions import MessageDecodeError, MessageSchemaError, MessageSchemaNotFound

logger = logging.getLogger(__name__)


class DefaultEncoder(JSONEncoder):
    def default(self, object_: Any) -> Any:

        if isinstance(object_, (datetime.date, datetime.datetime)):
            return object_.isoformat()

        elif isinstance(object_, UUID):
            return str(object_)

        return super().default(object_)


class JsonSchemaMixin:

    @property
    def message_schema(self) -> Dict:
        if not hasattr(self, "_message_schema"):
            raise MessageSchemaNotFound()

        return self._message_schema

    @message_schema.setter
    def message_schema(self, schema: Dict) -> None:
        self._message_schema = schema

    def decode_message(self, message: Union[str, bytes]) -> Dict:
        try:
            decoded_message: Dict = json.loads(message)
        except (json.JSONDecodeError) as e:
            raise MessageDecodeError(str(e))

        self.validate_message(decoded_message)

        return decoded_message

    def validate_message(self, message: Dict[str, Any]) -> None:
        try:
            if self.message_schema:
                jsonschema.validate(
                    instance=message,
                    schema=self.message_schema,
                    format_checker=jsonschema.draft7_format_checker,
                )
        except (
            jsonschema.exceptions.SchemaError,
            jsonschema.exceptions.ValidationError,
        ) as e:
            raise MessageSchemaError(str(e))

    def encode_message(self, message: Union[list, dict]) -> str:
        return json.dumps(message, cls=DefaultEncoder) if message else ''


class ErrorHandlerMixin:

    @abstractmethod
    def set_status(self, status_code: int, reason: Optional[str] = None) -> None:
        raise NotImplementedError

    @contextmanager
    def handle_error(self) -> Generator:
        try:
            yield

        except OpacException as e:
            code = e.code

            reason = f"[{code}] {e.message}: {e.detail}"

            if code >= 500:
                logger.critical(reason)
            else:
                logger.error(reason)

            self.set_status(code)

        except Exception as e:
            code = 500

            reason = f"[{code}] Error: {e!s}"

            logger.critical(reason)

            self.set_status(code)
