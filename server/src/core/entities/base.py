from dataclasses import asdict, field
from typing import Dict, Any, Set


class BaseEntity:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CollateResult(BaseEntity):
    new: Set[BaseEntity] = field(default_factory=set)
    updated: Set[BaseEntity] = field(default_factory=set)
    deleted: Set[BaseEntity] = field(default_factory=set)
