from dataclasses import dataclass
from src.core.entities.base import BaseEntity
from typing import Optional


@dataclass
class Book(BaseEntity):
    title: str
    subtitle: Optional[str]
    original_title: Optional[str]
    author: str
    category: Optional[str]
    pages: Optional[int]
    isbn: Optional[str]
    release: Optional[str]
