from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.base import Model
from src.dataproviders.db.types import Types


class EntityModel(Model):
    __abstract__ = True

    _pk: Mapped[int] = mapped_column(Types.BIGINT, primary_key=True)

    uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True, unique=True)
