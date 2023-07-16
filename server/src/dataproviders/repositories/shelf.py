from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.dialects import sqlite

from src.core.entities import Profile, Shelf
from src.core.repositories import IShelfRepository
from src.dataproviders.db import ShelfModel
from src.dataproviders.repositories.entity import EntityRepository


class ShelfRepository(IShelfRepository, EntityRepository[Shelf, ShelfModel]):
    def __init__(self) -> None:
        super().__init__(entity=Shelf, model=ShelfModel)

    def to_entity(self, model: ShelfModel) -> Shelf:
        return Shelf(
            profile_uuid=model.profile_uuid,
            name=model.name,
            value=model.value,
            pages=model.pages,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def read_all_for_profile(self, profile: Profile) -> List[Shelf]:
        stmt = select(self.model).where(self.model.profile_uuid == profile.uuid)
        models = self._db.session.scalars(stmt)

        return [self.to_entity(model) for model in models]

    async def sync_on_profile(self, profile: Profile, shelves: Sequence[Shelf]) -> List[Shelf]:
        stmt = sqlite.insert(self.model).values(  # type: ignore
            [self.to_mapping(shelf) for shelf in shelves]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[self.model.uuid],
            set_=dict(
                name=stmt.excluded.name,
                pages=stmt.excluded.pages,
            ),
        )

        self._db.session.execute(stmt)

        return list(shelves)
