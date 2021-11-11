import re
from dataclasses import dataclass, field
from typing import TypeVar

from src.core.entities.base import BaseEntity


T = TypeVar('T', bound="Book")


@dataclass
class Book(BaseEntity):
    book_id: str = field(init=False)
    title: str
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self.isbn = re.sub(r'[^X\d]+', '', self.isbn)

        self.book_id = self.id_from_attributes(self.title, self.author, self.isbn)

    def __hash__(self) -> int:
        return hash(self.book_id)

    def __lt__(self, other: T) -> bool:
        return hash(self) < hash(other)
