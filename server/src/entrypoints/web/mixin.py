import json
import datetime
from json import JSONEncoder
from typing import Any, Dict, Union

import jsonschema

from src.entrypoints.exceptions import MessageDecodeError, MessageSchemaNotDefined


class DefaultEncoder(JSONEncoder):
    def default(self, object_):

        if isinstance(object_, (datetime.date, datetime.datetime)):
            return object_.isoformat()

        return super().default(object_)


class JsonSchemaMixin:

    @property
    def message_schema(self) -> Dict:
        if not hasattr(self, "_message_schema"):
            raise MessageSchemaNotDefined

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
            raise MessageDecodeError(str(e))

    def encode_message(self, message: Union[list, dict]) -> str:
        return json.dumps(message, cls=DefaultEncoder) if message else ''
