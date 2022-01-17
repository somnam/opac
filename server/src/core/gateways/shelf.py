from abc import ABC, abstractmethod
from typing import Iterator

from src.core.entities import Profile, Shelf, ShelfItem


class IShelfGateway(ABC):

    @abstractmethod
    async def search(self, profile: Profile) -> Iterator[Shelf]:
        raise NotImplementedError()

    @abstractmethod
    async def items(self, profile: Profile, shelf: Shelf) -> Iterator[ShelfItem]:
        raise NotImplementedError()
