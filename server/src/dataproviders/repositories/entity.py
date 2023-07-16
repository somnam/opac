from abc import abstractmethod
from typing import Generic, List, Optional, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from src.config import Config
from src.core.repositories import IEntityRepository
from src.core.types import TEntity
from src.dataproviders.repositories.base import BaseRepository
from src.dataproviders.types import TEntityModel

config = Config()


class EntityRepository(BaseRepository, IEntityRepository, Generic[TEntity, TEntityModel]):
    model: Type[TEntityModel]

    def __init__(self, entity: Type[TEntity], model: Type[TEntityModel]) -> None:
        self.entity = entity
        self.model = model

    @abstractmethod
    def to_entity(self, model: TEntityModel) -> TEntity:
        ...

    def to_mapping(self, entity: TEntity) -> dict:
        return entity.dict()

    async def exists(self, uuid: UUID) -> bool:
        stmt = select(self.model._pk).where(self.model.uuid == uuid).exists()
        return bool(self._db.session.scalar(select(stmt)))

    async def create(self, entity: TEntity) -> None:
        await self.create_many((entity,))

    async def read(self, uuid: UUID) -> Optional[TEntity]:
        stmt = select(self.model).where(self.model.uuid == uuid)
        model = self._db.session.scalar(stmt)

        return self.to_entity(model) if model else None

    async def update(self, entity: TEntity) -> None:
        await self.update_many((entity,))

    async def delete(self, entity: TEntity) -> int:
        return await self.delete_many((entity,))

    async def read_all(self) -> List[TEntity]:
        models = self._db.session.scalars(select(self.model))
        return [self.to_entity(model) for model in models]

    async def create_many(self, entities: Sequence[TEntity]) -> None:
        if not entities:
            return

        mappings = [self.to_mapping(entity) for entity in entities]

        self._db.session.execute(insert(self.model), mappings)

    async def update_many(self, entities: Sequence[TEntity]) -> None:
        if not entities:
            return

        mappings = [self.to_mapping(entity) for entity in entities]

        self._db.session.execute(update(self.model), mappings)

    async def delete_many(self, entities: Sequence[TEntity]) -> int:
        if not entities:
            return 0

        uuids = [entity.uuid for entity in entities]

        self._db.session.execute(delete(self.model).where(self.entity.uuid.in_(uuids)))

        return len(entities)
