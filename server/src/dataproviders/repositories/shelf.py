from typing import List

from src.core.entities import Profile, Shelf
from src.core.repositories import ShelfRepositoryInterface
from src.dataproviders.db import ShelfModel
from src.dataproviders.repositories.base import BaseDbRepository


class ShelfRepository(BaseDbRepository, ShelfRepositoryInterface):
    def exists(self, shelf_id: str) -> bool:
        exists = self._dbh.session.query(ShelfModel._pk).filter_by(shelf_id=shelf_id).exists()
        result: bool = self._dbh.session.query(exists).scalar()
        return result

    def read_all(self, profile: Profile) -> List[Shelf]:
        models = self._dbh.session.query(ShelfModel)\
            .filter_by(profile_id=profile.profile_id)\
            .all()

        return [Shelf(
            name=model.name,
            value=model.value,
            profile_id=model.profile_id,
            pages=model.pages,
            refreshed_at=model.refreshed_at,
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

    def update(self, shelf: Shelf) -> None:
        model = self._dbh.session.query(ShelfModel)\
            .filter_by(shelf_id=shelf.shelf_id)\
            .one_or_none()

        if model:
            model.pages = shelf.pages
            model.refreshed_at = shelf.refreshed_at

    def update_all(self, shelves: List[Shelf]) -> None:
        if not shelves:
            return

        for shelf in shelves:
            self.update(shelf)

    def delete_all(self, shelves: List[Shelf]) -> None:
        if not shelves:
            return

        ids = (shelf.shelf_id for shelf in shelves)

        self._dbh.session.query(ShelfModel)\
            .filter(ShelfModel.shelf_id.in_(ids))\
            .delete(synchronize_session=False)
