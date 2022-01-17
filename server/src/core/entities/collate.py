from dataclasses import dataclass, field
from typing import List

from src.core.entities.entity import Entity


@dataclass
class Collate(Entity):
    new: List[Entity] = field(default_factory=list)
    updated: List[Entity] = field(default_factory=list)
    deleted: List[Entity] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.new or self.updated or self.deleted)
