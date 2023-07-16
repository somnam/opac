from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.entity import EntityModel
from src.dataproviders.db.model.mixin import CreatedAtMixin
from src.dataproviders.db.types import Types


class ShelfItemModel(EntityModel, CreatedAtMixin):
    __tablename__ = "shelf_item"

    profile_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)
    shelf_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)

    title: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    author: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    value: Mapped[str] = mapped_column(Types.EXTERNAL_ID, nullable=False)
