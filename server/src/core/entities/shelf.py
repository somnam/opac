from typing import List
from dataclasses import dataclass, field
from src.core.entities.base import BaseEntity
from src.core.entities.search_result import SearchResult
from src.core.entities.profile import Profile


@dataclass
class Shelf(BaseEntity):
    name: str
    value: str
    profile_value: str
    pages: int = 1


@dataclass
class ShelfSearchParams(BaseEntity):
    profile: Profile
    page: int = 1


@dataclass
class ShelfSearchResult(SearchResult):
    items: List[Shelf] = field(default_factory=list)
