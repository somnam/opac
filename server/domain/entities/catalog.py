from dataclasses import dataclass
from domain.entities.base import BaseEntity


@dataclass
class Catalog(BaseEntity):
    name: str
    city: str
    value: str
