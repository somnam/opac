from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from src.core.entities.entity import Entity
from src.core.entities.mixin import CreatedUpdatedAtMixin
from src.core.entities.search_result import SearchResult


@dataclass(eq=False, kw_only=True)
class Shelf(Entity, CreatedUpdatedAtMixin):
    profile_uuid: UUID
    name: str
    value: str
    pages: int = 1

    def __post_init__(self) -> None:
        super().__post_init__()
        self.uuid = self.get_uuid(self.profile_uuid, self.value)


@dataclass
class ShelfSearchParams(Entity):
    profile_uuid: UUID
    shelf_uuids: list[UUID] = field(default_factory=list)
    page: int = 1


@dataclass
class ShelfSearchResult(SearchResult[Shelf]):
    items: List[Shelf] = field(default_factory=list)
