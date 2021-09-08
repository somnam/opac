from dataclasses import asdict, dataclass, field
from typing import Dict, Any, Set
from hashlib import md5


class BaseEntity:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def id_from_attributes(cls, *attrs: str) -> str:
        encoded_attrs = "+".join((str(attr) for attr in attrs)).encode('utf-8')

        return md5(encoded_attrs).hexdigest()


@dataclass
class CollateResult(BaseEntity):
    new: Set[BaseEntity] = field(default_factory=set)
    updated: Set[BaseEntity] = field(default_factory=set)
    deleted: Set[BaseEntity] = field(default_factory=set)

    def __bool__(self) -> bool:
        return bool(self.new or self.updated or self.deleted)
