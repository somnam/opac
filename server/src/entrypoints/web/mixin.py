import json
from typing import Dict, Union

import jsonschema
from src.entrypoints.exceptions import MessageDecodeError, MessageSchemaNotDefined


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

            if self.message_schema:
                jsonschema.validate(
                    instance=decoded_message,
                    schema=self.message_schema,
                    format_checker=jsonschema.draft7_format_checker,
                )
        except (
            json.JSONDecodeError,
            jsonschema.exceptions.SchemaError,
            jsonschema.exceptions.ValidationError,
        ) as e:
            raise MessageDecodeError(str(e))

        return decoded_message

    def encode_message(self, message: Union[list, dict]) -> str:
        return json.dumps(message) if message else ''
