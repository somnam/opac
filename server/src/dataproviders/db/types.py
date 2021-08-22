# import json

import sqlalchemy as sa
import sqlalchemy_utils as su


# class JsonType(sa.TypeDecorator):
#     """Enables JSON storage for sqlite with no extensions."""
#     impl = sa.Text

#     def process_bind_param(self, value, dialect):
#         return json.dumps(value)

#     def process_result_value(self, value, dialect):
#         try:
#             return json.loads(value)
#         except (ValueError, TypeError):
#             return None


class Types:
    ENUM = sa.Enum
    BOOL = sa.Boolean
    URL = sa.String(2083)
    ISBN = sa.String(13)
    UUID = su.UUIDType(binary=True)
    MD5 = sa.CHAR(32)
    EXTERNAL_ID = sa.CHAR(32)
    VARCHAR = sa.String
    INT = sa.Integer
    BIGINT = sa.BigInteger
    NUMERIC = sa.Numeric
    # JSON = JsonType
    JSON = sa.JSON
    DATE = sa.Date
    DATETIME = sa.DateTime(timezone=True)
