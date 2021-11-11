from abc import ABC, abstractmethod
from typing import ContextManager, Sequence

from src.core.entities import BaseEntity, CollateResult


class BaseRepository(ABC):
    @abstractmethod
    def unit_of_work(self) -> ContextManager:
        raise NotImplementedError

    @abstractmethod
    def collate(self, items: Sequence[BaseEntity], current_items: Sequence[BaseEntity]) -> CollateResult:
        raise NotImplementedError
