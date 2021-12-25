import sqlalchemy as sa
import sqlalchemy_utils as su

from sqlalchemy import Integer


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
    BIGINT = sa.BigInteger().with_variant(Integer, "sqlite")
    NUMERIC = sa.Numeric
    # JSON = JsonType
    JSON = sa.JSON
    DATE = sa.Date
    DATETIME = sa.DateTime(timezone=True)
