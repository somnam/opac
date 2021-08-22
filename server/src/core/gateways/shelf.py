from abc import ABC, abstractmethod
from typing import List, Set

from src.core.entities import Shelf, ShelfSearchParams, ShelfItem


class ShelfGatewayInterface(ABC):

    @abstractmethod
    async def search(self, params: ShelfSearchParams) -> List[Shelf]:
        raise NotImplementedError()

    @abstractmethod
    async def items(self, shelf: Shelf) -> Set[ShelfItem]:
        raise NotImplementedError()
