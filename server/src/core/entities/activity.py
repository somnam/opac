from dataclasses import dataclass
from src.core.entities.base import BaseEntity


@dataclass
class Activity(BaseEntity):
    name: str
    value: str
    caller: str
