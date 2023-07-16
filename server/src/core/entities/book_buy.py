from dataclasses import dataclass, field
from typing import List
from urllib.parse import parse_qs, urlparse

from src.core.entities.entity import Entity
from src.core.entities.mixin import IsbnMixin, UrlMixin


@dataclass(eq=False, kw_only=True)
class BookBuyUrl(Entity, UrlMixin, IsbnMixin):
    isbn_list: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.uri)
        self.isbn_list = self.get_isbn_list()

    def get_isbn_list(self) -> List[str]:
        query = parse_qs(urlparse(self.uri).query)
        return [self.normalize_isbn(isbn) for isbn in query.get("number[]", [])]
