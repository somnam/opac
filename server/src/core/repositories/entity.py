from abc import abstractmethod
from typing import Any, Collection, Generic, Iterator, Optional, Type
from uuid import UUID

from src.core.repositories.base import IRepository
from src.core.types import TEntity


class IEntityRepository(IRepository, Generic[TEntity]):
    entity: Type[TEntity]

    @abstractmethod
    def exists(self, uuid: UUID) -> bool:
        raise NotImplementedError

    def create(self, entity: TEntity) -> TEntity:
        return next(self.create_collection((entity,)))

    def read(self, **kwargs: Any) -> Optional[TEntity]:
        return next(self.search(**kwargs), None)

    def update(self, entity: TEntity) -> TEntity:
        return next(self.update_collection((entity,)))

    def delete(self, entity: TEntity) -> int:
        return self.delete_collection((entity,))

    @abstractmethod
    def search(self, **kwargs: Any) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def create_collection(self, entities: Collection[TEntity]) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_collection(self, entities: Collection[TEntity]) -> Iterator[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_collection(self, entities: Collection[TEntity]) -> int:
        raise NotImplementedError
