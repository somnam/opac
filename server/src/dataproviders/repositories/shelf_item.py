from typing import List

from src.core.entities import Shelf, ShelfItem
from src.core.repositories import ShelfItemRepositoryInterface
from src.dataproviders.db import ShelfItemModel
from src.dataproviders.repositories.base import BaseDbRepository


class ShelfItemRepository(BaseDbRepository, ShelfItemRepositoryInterface):

    def read_all(self, shelf: Shelf) -> List[ShelfItem]:
        query = self._dbh.session.query(*ShelfItemModel.columns())\
            .filter_by(shelf_id=shelf.shelf_id)

        return [
            ShelfItem(
                book_id=row.book_id,
                shelf_id=row.shelf_id,
                title=row.title,
                author=row.author,
                isbn=row.isbn,
                subtitle=row.subtitle,
                original_title=row.original_title,
                category=row.category,
                pages=row.pages,
                release=row.release,
            )
            for row in query
        ]

    def create_all(self, items: List[ShelfItem]) -> None:
        if not items:
            return

        self._dbh.session.bulk_save_objects([
            ShelfItemModel(
                shelf_item_id=item.shelf_item_id,
                book_id=item.book_id,
                shelf_id=item.shelf_id,
                title=item.title,
                author=item.author,
                isbn=item.isbn,
                subtitle=item.subtitle,
                original_title=item.original_title,
                category=item.category,
                pages=item.pages,
                release=item.release,
            )
            for item in items
        ])

    def delete_all(self, items: List[ShelfItem]) -> None:
        if not items:
            return

        ids = (item.shelf_item_id for item in items)

        self._dbh.session.query(ShelfItemModel)\
            .filter(ShelfItemModel.shelf_item_id.in_(ids))\
            .delete(synchronize_session=False)
