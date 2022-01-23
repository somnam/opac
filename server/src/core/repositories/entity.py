from abc import abstractmethod
from typing import Any, Generic, Iterator, Optional, Sequence, Type
from uuid import UUID

from src.core.repositories.base import IRepository
from src.core.types import TEntity


class IEntityRepository(IRepository, Generic[TEntity]):
    entity: Type[TEntity]

    @abstractmethod
    def exists(self, uuid: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def read(self, **kwargs: Any) -> Optional[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: TEntity) -> int:
        raise NotImplementedError

    @abstractmethod
    def search(self, **kwargs: Any) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def create_many(self, entities: Sequence[TEntity]) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_many(self, entities: Sequence[TEntity]) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_many(self, entities: Sequence[TEntity]) -> int:
        raise NotImplementedError
