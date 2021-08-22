from dataclasses import dataclass, field
from hashlib import md5
from typing import Optional

from src.core.entities.base import BaseEntity


@dataclass
class BookMeta(BaseEntity):
    subtitle: Optional[str] = None
    original_title: Optional[str] = None
    category: Optional[str] = None
    pages: Optional[int] = None
    release: Optional[str] = None


@dataclass
class Book(BaseEntity):
    book_id: str = field(init=False)
    title: str
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self.book_id = md5("+".join((self.title, self.author, self.isbn)).encode('utf-8')).hexdigest()
