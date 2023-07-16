from dataclasses import asdict, dataclass, field, replace
from typing import Any, Dict
from uuid import NAMESPACE_DNS, UUID, uuid4, uuid5


@dataclass(eq=False, kw_only=True)
class Entity:
    uuid: UUID = field(init=False, default_factory=uuid4)

    @staticmethod
    def get_uuid(*attrs: Any) -> UUID:
        return uuid5(NAMESPACE_DNS, "+".join(str(attr) for attr in attrs))

    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    def copy(self, **changes: Any) -> Any:
        return replace(self, **changes)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and hash(self) == hash(other)

    def __lt__(self, other: object) -> bool:
        return type(self) == type(other) and hash(self) < hash(other)
