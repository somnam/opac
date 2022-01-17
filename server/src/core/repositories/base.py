from abc import ABC, abstractmethod
from typing import ContextManager, Iterator

from src.core.entities import Entity, Collate


class IRepository(ABC):
    @abstractmethod
    def unit_of_work(self) -> ContextManager:
        raise NotImplementedError

    @abstractmethod
    def collate(self, items: Iterator[Entity], current_items: Iterator[Entity]) -> Collate:
        raise NotImplementedError
