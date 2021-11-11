from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Shelf, Profile, ShelfItem


class ShelfGatewayInterface(ABC):

    @abstractmethod
    async def search(self, profile: Profile) -> List[Shelf]:
        raise NotImplementedError()

    @abstractmethod
    async def items(self, profile: Profile, shelf: Shelf) -> List[ShelfItem]:
        raise NotImplementedError()
