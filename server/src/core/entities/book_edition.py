from dataclasses import dataclass
from uuid import UUID

from src.core.entities.entity import Entity
from src.core.entities.mixin import CreatedAtMixin, IsbnMixin


@dataclass(eq=False, kw_only=True)
class BookEdition(Entity, IsbnMixin, CreatedAtMixin):
    profile_uuid: UUID
    shelf_uuid: UUID
    shelf_item_uuid: UUID
    title: str
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self.isbn = self.normalize_isbn(self.isbn)
        self.uuid = self.get_uuid(self.shelf_item_uuid, self.isbn)
