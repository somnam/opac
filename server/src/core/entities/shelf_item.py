from dataclasses import dataclass, field
from typing import Optional
from datetime import date

from src.core.entities.base import BaseEntity
from src.core.entities.book import Book


@dataclass
class ShelfItem(BaseEntity):
    shelf_item_id: str = field(init=False)
    book_id: str
    shelf_id: str
    title: str
    author: str
    isbn: str
    subtitle: Optional[str] = None
    original_title: Optional[str] = None
    category: Optional[str] = None
    pages: Optional[int] = None
    release: Optional[date] = None

    def __post_init__(self) -> None:
        self.shelf_item_id = self.id_from_attributes(self.book_id, self.shelf_id)

    def __hash__(self) -> int:
        return hash(self.shelf_item_id)

    @property
    def book(self) -> Book:
        return Book(
            title=self.title,
            author=self.author,
            isbn=self.isbn,
        )
