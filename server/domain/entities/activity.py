from dataclasses import dataclass
from domain.entities.base import BaseEntity


@dataclass
class Activity(BaseEntity):
    name: str
    value: str
    caller: str
