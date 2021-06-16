from dataclasses import dataclass
from src.core.entities.base import BaseEntity


@dataclass
class Catalog(BaseEntity):
    name: str
    city: str
    value: str
