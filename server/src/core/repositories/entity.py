from abc import abstractmethod
from typing import Generic, List, Optional, Sequence, Type
from uuid import UUID

from src.core.repositories.base import IRepository
from src.core.types import TEntity


class IEntityRepository(IRepository, Generic[TEntity]):
    entity: Type[TEntity]

    @abstractmethod
    async def exists(self, uuid: UUID) -> bool:
        ...

    @abstractmethod
    async def create(self, entity: TEntity) -> None:
        ...

    @abstractmethod
    async def read(self, uuid: UUID) -> Optional[TEntity]:
        ...

    @abstractmethod
    async def update(self, entity: TEntity) -> None:
        ...

    @abstractmethod
    async def delete(self, entity: TEntity) -> int:
        ...

    @abstractmethod
    async def read_all(self) -> List[TEntity]:
        ...

    @abstractmethod
    async def create_many(self, entities: Sequence[TEntity]) -> None:
        ...

    @abstractmethod
    async def update_many(self, entities: Sequence[TEntity]) -> None:
        ...

    @abstractmethod
    async def delete_many(self, entities: Sequence[TEntity]) -> int:
        ...
