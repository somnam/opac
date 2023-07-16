from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.entity import EntityModel
from src.dataproviders.db.model.mixin import CreatedAtMixin
from src.dataproviders.db.types import Types


class BookEditionModel(EntityModel, CreatedAtMixin):
    __tablename__ = "book_edition"

    profile_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)
    shelf_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)
    shelf_item_uuid: Mapped[UUID] = mapped_column(Types.UUID, nullable=False, index=True)

    title: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    author: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    isbn: Mapped[str] = mapped_column(Types.ISBN, nullable=False, index=True)
