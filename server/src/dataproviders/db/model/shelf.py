from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.entity import EntityModel
from src.dataproviders.db.model.mixin import CreatedUpdatedAtMixin
from src.dataproviders.db.types import Types


class ShelfModel(EntityModel, CreatedUpdatedAtMixin):
    __tablename__ = "shelf"

    profile_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)

    name: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    value: Mapped[str] = mapped_column(Types.EXTERNAL_ID, nullable=False)
    pages: Mapped[int] = mapped_column(Types.INT, nullable=False)
