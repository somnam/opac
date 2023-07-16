import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from urllib.parse import urlsplit


class IsbnMixin:
    @staticmethod
    def normalize_isbn(isbn: str) -> str:
        return re.sub(r"[^X\d]+", "", isbn)


@dataclass(eq=False, kw_only=True)
class UrlMixin:
    uri: str

    def __post_init__(self) -> None:
        self.uri = urlsplit(self.uri).geturl()


@dataclass(kw_only=True)
class CreatedAtMixin:
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(kw_only=True)
class CreatedUpdatedAtMixin(CreatedAtMixin):
    updated_at: Optional[datetime] = field(default=None, compare=False)

    def __post_init__(self) -> None:
        if self.updated_at is None:
            self.updated_at = self.created_at
