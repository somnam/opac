from typing import List
from domain.entities.base import BaseEntity
from domain.entities.search_results import SearchResults
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
class ProfileSearchResults(SearchResults):
    items: List[Profile] = field(default_factory=list)
