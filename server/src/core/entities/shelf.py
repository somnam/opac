from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.core.entities.base import BaseEntity
from src.core.entities.search_result import SearchResult
from src.core.entities.profile import Profile


@dataclass
class Shelf(BaseEntity):
    shelf_id: str = field(init=False)
    profile_id: str
    name: str
    value: str
    pages: int = 1
    refreshed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.shelf_id = self.id_from_attributes(self.profile_id, self.value)

    def __hash__(self) -> int:
        return hash(self.shelf_id)


@dataclass
class ShelfSearchParams(BaseEntity):
    profile: Profile
    page: int = 1


@dataclass
class ShelfSearchResult(SearchResult):
    items: List[Shelf] = field(default_factory=list)
