from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Shelf, ShelvesSearchParams, Book


class ShelvesGatewayInterface(ABC):

    @abstractmethod
    async def search(self, params: ShelvesSearchParams) -> List[Shelf]:
        raise NotImplementedError()

    @abstractmethod
    async def books(self, shelf: Shelf) -> List[Book]:
        raise NotImplementedError()
