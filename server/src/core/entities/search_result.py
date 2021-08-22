from typing import List, Any
from dataclasses import dataclass, field
from src.core.entities.base import BaseEntity


@dataclass
class SearchResult(BaseEntity):
    items: List[Any] = field(default_factory=list)
    page: int = 1
    prev_page: int = 0
    next_page: int = 0
    total: int = 0

    def __post_init__(self) -> None:
        if self.total == 0:
            self.total = len(self.items)

        if self.page > 1:
            self.prev_page = self.page - 1

        if self.total > (self.page * 10):
            self.next_page = self.page + 1
