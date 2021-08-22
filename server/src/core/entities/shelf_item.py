from dataclasses import dataclass

from src.core.entities.base import BaseEntity
from src.core.entities.book import Book, BookMeta


@dataclass
class ShelfItem(BaseEntity):
    book: Book
    metadata: BookMeta
