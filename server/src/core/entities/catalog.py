from dataclasses import dataclass

from src.core.entities.entity import Entity


@dataclass(eq=False, kw_only=True)
class Catalog(Entity):
    name: str
    city: str
    value: str

    def __post_init__(self) -> None:
        self.uuid = self.get_uuid(self.value)
