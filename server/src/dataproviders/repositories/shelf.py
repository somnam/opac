from typing import List

from src.core.entities import Profile, Shelf
from src.core.repositories import ShelfRepositoryInterface
from src.dataproviders.mixin import DbHandlerMixin
from src.dataproviders.db import ShelfModel


class ShelfRepository(ShelfRepositoryInterface, DbHandlerMixin):
    def read_all(self, profile: Profile) -> List[Shelf]:
        models = self._dbh.session.query(ShelfModel)\
            .filter_by(profile_value=profile.value)\
            .all()

        return [Shelf(
            name=model.name,
            value=model.value,
            profile_value=model.profile_value,
            pages=model.pages,
        ) for model in models]

    def create_all(self, shelves: List[Shelf]) -> None:
        if not shelves:
            return

        self._dbh.session.bulk_save_objects([
            ShelfModel(
                name=shelf.name,
                value=shelf.value,
                profile_value=shelf.profile_value,
                pages=shelf.pages,
            ) for shelf in shelves
        ])
