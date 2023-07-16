from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core.entities.entity import Entity
from src.core.entities.mixin import IsbnMixin


@dataclass(eq=False, kw_only=True)
class LatestBook(Entity, IsbnMixin):
    catalog_uuid: UUID
    title: str
    author: str
    isbn: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.isbn = self.normalize_isbn(self.isbn)
        self.uuid = self.get_uuid(self.catalog_uuid, self.isbn)
