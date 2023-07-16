from dataclasses import dataclass, field
from uuid import UUID

from src.core.entities.book_edition import BookEdition
from src.core.entities.entity import Entity
from src.core.entities.mixin import CreatedAtMixin


@dataclass(eq=False, kw_only=True)
class ShelfItem(Entity, CreatedAtMixin):
    profile_uuid: UUID
    shelf_uuid: UUID
    title: str
    author: str
    value: str
    book_editions: list[BookEdition] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.shelf_uuid, self.value)
