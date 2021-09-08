from dataclasses import dataclass
from typing import List, Union

from src.core.entities.base import BaseEntity


@dataclass
class ScheduleItem(BaseEntity):
    delay: int
    args: List[Union[str, int, dict]]
