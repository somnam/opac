from typing import List

from src.core.entities import Profile, Shelf
from src.core.repositories import ShelfRepositoryInterface
from src.dataproviders.db import ShelfModel
from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.mixin import CollateMixin


class ShelfRepository(ShelfRepositoryInterface, BaseDbRepository, CollateMixin):
    def read_all(self, profile: Profile) -> List[Shelf]:
        models = self._dbh.session.query(ShelfModel)\
            .filter_by(profile_id=profile.profile_id)\
            .all()

        return [Shelf(
            name=model.name,
            value=model.value,
            profile_id=model.profile_id,
            pages=model.pages,
        ) for model in models]

    def create_all(self, shelves: List[Shelf]) -> None:
        if not shelves:
            return

        self._dbh.session.bulk_save_objects([
            ShelfModel(
                shelf_id=shelf.shelf_id,
                profile_id=shelf.profile_id,
                name=shelf.name,
                value=shelf.value,
                pages=shelf.pages,
            ) for shelf in shelves
        ])
