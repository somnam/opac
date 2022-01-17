from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from src.core.entities.entity import Entity


@dataclass
class ScheduleItem(Entity):
    delay: int = 0
    args: Optional[List[Union[str, int, dict]]] = None
    kwargs: Optional[Dict[str, Union[str, int, dict]]] = None
    job_id: Optional[str] = None
