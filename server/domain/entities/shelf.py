from typing import List
from dataclasses import dataclass, field
from domain.entities.base import BaseEntity
from domain.entities.profile import Profile


@dataclass
class Shelf(BaseEntity):
    name: str
    value: str


@dataclass
class ShelvesSearchParams(BaseEntity):
    profile: Profile
    page: int = 1


@dataclass
class ShelvesSearchResults(BaseEntity):
    items: List[Shelf] = field(default_factory=list)
    page: int = 1
    prev_page: int = 0
    next_page: int = 0

    def __post_init__(self) -> None:
        total = len(self.items)

        # Reduce items to 10 entries from current page.
        start_idx = (self.page - 1) * 10
        self.items = self.items[start_idx:start_idx + 10]

        if self.page > 1:
            self.prev_page = self.page - 1

        if total > (self.page * 10):
            self.next_page = self.page + 1
