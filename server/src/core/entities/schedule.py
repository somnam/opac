from dataclasses import dataclass
from typing import List, Dict, Union, Optional

from src.core.entities.base import BaseEntity


@dataclass
class ScheduleItem(BaseEntity):
    delay: int = 0
    args: Optional[List[Union[str, int, dict]]] = None
    kwargs: Optional[Dict[str, Union[str, int, dict]]] = None
    job_id: Optional[str] = None
