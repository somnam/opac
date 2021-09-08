import re
from dataclasses import dataclass, field

from src.core.entities.base import BaseEntity


@dataclass
class Book(BaseEntity):
    book_id: str = field(init=False)
    title: str
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self.isbn = re.sub(r'[^X\d]+', '', self.isbn)

        self.book_id = self.id_from_attributes(self.title, self.author, self.isbn)
