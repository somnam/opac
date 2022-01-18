from typing import Any, Callable, Collection, Generic, Iterator, Optional, Type
from uuid import UUID

from src.core.repositories import IEntityRepository
from src.core.types import TEntity
from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.types import TModel


class EntityRepository(BaseDbRepository, IEntityRepository, Generic[TEntity, TModel]):
    model: Type[TModel]

    def __init__(
        self,
        entity: Type[TEntity],
        model: Type[TModel],
        from_model: Callable[[TModel], TEntity],
    ) -> None:
        self.entity = entity
        self.model = model
        self.from_model = from_model

    def exists(self, uuid: UUID) -> bool:
        exists = self._dbh.session.query(self.model._pk).filter_by(uuid=uuid).exists()
        result: bool = self._dbh.session.query(exists).scalar()
        return result

    def create(self, entity: TEntity) -> TEntity:
        return next(self.create_collection((entity,)))

    def read(self, **kwargs: Any) -> Optional[TEntity]:
        return next(self.search(**kwargs), None)

    def update(self, entity: TEntity) -> TEntity:
        return next(self.update_collection((entity,)))

    def delete(self, entity: TEntity) -> int:
        return self.delete_collection((entity,))

    def search(self, **kwargs: Any) -> Iterator[TEntity]:
        models = self._dbh.session.query(*self.model.columns())\
            .filter_by(**kwargs)

        return iter([self.from_model(model) for model in models])

    def create_collection(self, entities: Collection[TEntity]) -> Iterator[TEntity]:
        if not entities:
            return iter([])

        self._dbh.session.bulk_insert_mappings(
            self.model,
            [entity.dict() for entity in entities]
        )

        return iter(entities)

    def update_collection(self, entities: Collection[TEntity]) -> Iterator[TEntity]:
        if not entities:
            return iter([])

        self._dbh.session.bulk_update_mappings(
            self.model,
            [entity.dict() for entity in entities]
        )

        return iter(entities)

    def delete_collection(self, entities: Collection[TEntity]) -> int:
        if not entities:
            return 0

        uuids = (entity.uuid for entity in entities)

        rows_count: int = self._dbh.session.query(self.model)\
            .filter(self.model.uuid.in_(uuids))\
            .delete(synchronize_session=False)

        return rows_count
