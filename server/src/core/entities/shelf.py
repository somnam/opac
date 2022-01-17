from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.core.entities.entity import Entity
from src.core.entities.profile import Profile
from src.core.entities.search_result import SearchResult


@dataclass(eq=False)
class Shelf(Entity):
    profile_uuid: UUID
    name: str
    value: str
    pages: int = 1
    refreshed_at: Optional[datetime] = field(default=None, compare=False)

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.profile_uuid, self.value)


@dataclass
class ShelfSearchParams(Entity):
    profile: Profile
    page: int = 1


@dataclass
class ShelfSearchResult(SearchResult):
    items: List[Shelf] = field(default_factory=list)
