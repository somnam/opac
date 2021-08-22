from typing import List
from src.core.entities.base import BaseEntity
from src.core.entities.search_result import SearchResult
from dataclasses import dataclass, field


@dataclass
class Profile(BaseEntity):
    name: str
    value: str


@dataclass
class ProfileSearchParams(BaseEntity):
    phrase: str
    page: int = 1


@dataclass
class ProfileSearchResult(SearchResult):
    items: List[Profile] = field(default_factory=list)
