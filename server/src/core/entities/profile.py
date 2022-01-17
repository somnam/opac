from dataclasses import dataclass, field
from typing import List

from src.core.entities.entity import Entity
from src.core.entities.search_result import SearchResult


@dataclass(eq=False)
class Profile(Entity):
    name: str
    value: str

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.name, self.value)


@dataclass
class ProfileSearchParams(Entity):
    phrase: str
    page: int = 1


@dataclass
class ProfileSearchResult(SearchResult):
    items: List[Profile] = field(default_factory=list)
