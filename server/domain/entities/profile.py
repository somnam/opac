from typing import List
from domain.entities.base import BaseEntity
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
class ProfileSearchResults(BaseEntity):
    items: List[Profile] = field(default_factory=list)
    page: int = 1
    prev_page: int = 0
    next_page: int = 0
    total: int = 0

    def __post_init__(self) -> None:
        if self.items and not self.total:
            self.total = len(self.items)

        if self.page > 1:
            self.prev_page = self.page - 1

        if self.total > (self.page * 10):
            self.next_page = self.page + 1
