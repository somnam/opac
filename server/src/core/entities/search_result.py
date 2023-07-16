from dataclasses import dataclass, field
from typing import Any, Generic, List

from src.core.entities.entity import Entity
from src.core.types import TEntity


@dataclass(kw_only=True)
class SearchResult(Entity, Generic[TEntity]):
    items: List[Any] = field(default_factory=list)
    page: int = 1
    per_page: int = 10
    prev_page: int = 0
    next_page: int = 0
    total: int = 0

    def __post_init__(self) -> None:
        if self.total == 0:
            self.total = len(self.items)

        if self.page > 1:
            self.prev_page = self.page - 1

        if self.total > (self.page * self.per_page):
            self.next_page = self.page + 1

        # Reduce items to 'per_gage' entries from current page.
        if len(self.items) > self.per_page:
            start_idx = (self.page - 1) * self.per_page
            self.items = self.items[start_idx : start_idx + self.per_page]

    def first(self) -> TEntity | None:
        return self.items[0] if self.items else None
