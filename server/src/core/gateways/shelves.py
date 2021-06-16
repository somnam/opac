from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Shelf, ShelvesSearchParams


class ShelvesGatewayInterface(ABC):

    @abstractmethod
    async def search(self, params: ShelvesSearchParams) -> List[Shelf]:
        raise NotImplementedError()
