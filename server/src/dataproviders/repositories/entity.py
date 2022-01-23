from typing import Any, Callable, Generic, Iterator, Optional, Sequence, Type
from uuid import UUID

from src.config import Config
from src.core.repositories import IEntityRepository
from src.core.types import TEntity
from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.types import TModel

config = Config()


class EntityRepository(BaseDbRepository, IEntityRepository, Generic[TEntity, TModel]):
    model: Type[TModel]

    _batch_size = config.getint('repository', 'batch_size')

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
        return next(self.create_many((entity,)))

    def read(self, **kwargs: Any) -> Optional[TEntity]:
        return next(self.search(**kwargs), None)

    def update(self, entity: TEntity) -> TEntity:
        return next(self.update_many((entity,)))

    def delete(self, entity: TEntity) -> int:
        return self.delete_many((entity,))

    def search(self, **kwargs: Any) -> Iterator[TEntity]:
        models = self._dbh.session.query(*self.model.columns())\
            .filter_by(**kwargs)

        return iter([self.from_model(model) for model in models])

    def create_many(self, entities: Sequence[TEntity]) -> Iterator[TEntity]:
        if not entities:
            return iter([])

        self._dbh.session.bulk_insert_mappings(
            self.model,
            [entity.dict() for entity in entities]
        )

        return iter(entities)

    def update_many(self, entities: Sequence[TEntity]) -> Iterator[TEntity]:
        if not entities:
            return iter([])

        batches = (entities[step:step + self._batch_size]
                   for step in range(0, len(entities), self._batch_size))

        for batch in batches:

            entities_by_uuid = {entity.uuid: entity for entity in batch}

            models = self._dbh.session.query(self.model._pk, self.model.uuid)\
                .filter(self.model.uuid.in_(entities_by_uuid.keys()))

            mappings = []
            for model in models:
                mapping = dict(model)
                mapping.update(entities_by_uuid[model.uuid].dict())

                mappings.append(mapping)

            self._dbh.session.bulk_update_mappings(self.model, mappings)

        return iter(entities)

    def delete_many(self, entities: Sequence[TEntity]) -> int:
        if not entities:
            return 0

        batches = (entities[step:step + self._batch_size]
                   for step in range(0, len(entities), self._batch_size))

        rows_count = 0

        for batch in batches:

            uuids = (entity.uuid for entity in batch)

            rows_count += self._dbh.session.query(self.model)\
                .filter(self.model.uuid.in_(uuids))\
                .delete(synchronize_session=False)

        return rows_count
