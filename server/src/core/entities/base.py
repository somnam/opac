from dataclasses import asdict
from typing import Dict, Any


class BaseEntity:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
