from dataclasses import dataclass, field
from typing import List

from src.core.entities.entity import Entity
from src.core.entities.mixin import CreatedAtMixin
from src.core.entities.search_result import SearchResult


@dataclass(eq=False, kw_only=True)
class Profile(Entity, CreatedAtMixin):
    name: str
    value: str

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.value)


@dataclass(kw_only=True)
class ProfileSearchParams(Entity):
    phrase: str
    page: int = 1


@dataclass(kw_only=True)
class ProfileSearchResult(SearchResult):
    items: List[Profile] = field(default_factory=list)
