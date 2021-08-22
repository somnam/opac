from typing import Any
from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.models import generic_repr
from src.dataproviders.db.types import Types


@generic_repr
class DeclarativeBase(Types):
    @classmethod
    def columns(cls) -> Any:
        '''List table columns.'''
        return inspect(cls).mapper.columns.values()


Model = declarative_base(
    cls=DeclarativeBase,
    metadata=MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })
)
