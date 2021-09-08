from typing import List
from src.core.entities.base import BaseEntity
from src.core.entities.search_result import SearchResult
from dataclasses import dataclass, field


@dataclass
class Profile(BaseEntity):
    profile_id: str = field(init=False)
    name: str
    value: str

    def __post_init__(self) -> None:
        self.profile_id = self.id_from_attributes(self.value)

    def __hash__(self) -> int:
        return hash(self.profile_id)


@dataclass
class ProfileSearchParams(BaseEntity):
    phrase: str
    page: int = 1


@dataclass
class ProfileSearchResult(SearchResult):
    items: List[Profile] = field(default_factory=list)
