from dataclasses import dataclass, field
from src.core.entities.base import BaseEntity


@dataclass
class Catalog(BaseEntity):
    catalog_id: str = field(init=False)
    name: str
    city: str
    value: str

    def __post_init__(self) -> None:
        self.catalog_id = self.id_from_attributes(self.value)
