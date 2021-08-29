from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Profile, Shelf


class ShelfRepositoryInterface(ABC):
    @abstractmethod
    def read_all(self, profile: Profile) -> List[Shelf]:
        raise NotImplementedError

    @abstractmethod
    def create_all(self, shelves: List[Shelf]) -> None:
        raise NotImplementedError
