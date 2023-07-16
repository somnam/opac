from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.entity import EntityModel
from src.dataproviders.db.model.mixin import CreatedAtMixin
from src.dataproviders.db.types import Types


class LatestBookModel(EntityModel, CreatedAtMixin):
    __tablename__ = "latest_book"

    catalog_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)

    title: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    author: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    isbn: Mapped[str] = mapped_column(Types.ISBN, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        Types.DATETIME, nullable=False, default=datetime.utcnow
    )
