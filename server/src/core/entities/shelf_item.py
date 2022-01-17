from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from src.core.entities.book import Book
from src.core.entities.entity import Entity


@dataclass(eq=False)
class ShelfItem(Entity):
    book_uuid: UUID
    shelf_uuid: UUID
    title: str
    author: str
    isbn: str
    subtitle: Optional[str] = None
    original_title: Optional[str] = None
    category: Optional[str] = None
    pages: Optional[int] = None
    release: Optional[date] = None

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.book_uuid, self.shelf_uuid)

    @property
    def book(self) -> Book:
        return Book(
            title=self.title,
            author=self.author,
            isbn=self.isbn,
        )
