from abc import ABC, abstractmethod
from typing import AsyncContextManager, Generic

from src.core.types import TEntity


class IRepository(ABC):
    @abstractmethod
    def context(self) -> AsyncContextManager:
        ...


class IEntityMapper(ABC, Generic[TEntity]):
    @abstractmethod
    def to_entity(self) -> TEntity:
        raise NotImplementedError
