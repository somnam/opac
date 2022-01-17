import re
from dataclasses import dataclass

from src.core.entities.entity import Entity


@dataclass
class Book(Entity):
    title: str
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self.isbn = re.sub(r'[^X\d]+', '', self.isbn)

        self.uuid = self.get_uuid(self.title, self.author, self.isbn)
