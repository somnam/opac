import logging
from typing import List, Sequence

from sqlalchemy import delete, select
from sqlalchemy.dialects import sqlite

from src.core.entities.shelf import Shelf
from src.core.entities.shelf_item import ShelfItem
from src.core.repositories.shelf_item import IShelfItemRepository
from src.dataproviders.db.model.shelf_item import ShelfItemModel
from src.dataproviders.repositories.entity import EntityRepository

logger = logging.getLogger(__name__)


class ShelfItemRepository(IShelfItemRepository, EntityRepository[ShelfItem, ShelfItemModel]):
    def __init__(self) -> None:
        super().__init__(entity=ShelfItem, model=ShelfItemModel)

    def to_entity(self, model: ShelfItemModel) -> ShelfItem:
        return ShelfItem(
            profile_uuid=model.profile_uuid,
            shelf_uuid=model.shelf_uuid,
            title=model.title,
            author=model.author,
            value=model.value,
            created_at=model.created_at,
        )

    def to_mapping(self, entity: ShelfItem) -> dict:
        return {
            "uuid": entity.uuid,
            "profile_uuid": entity.profile_uuid,
            "shelf_uuid": entity.shelf_uuid,
            "title": entity.title,
            "author": entity.author,
            "value": entity.value,
            "created_at": entity.created_at,
        }

    async def read_all_on_shelf(self, shelf: Shelf) -> List[ShelfItem]:
        stmt = select(self.model).where(self.model.shelf_uuid == shelf.uuid)
        models = self._db.session.scalars(stmt)

        return [self.to_entity(model) for model in models]

    async def sync_on_shelf(self, shelf: Shelf, shelf_items: Sequence[ShelfItem]) -> None:
        if not shelf_items:
            return

        delete_stmt = delete(self.model).where(
            self.model.shelf_uuid == shelf.uuid,
            self.model.uuid.not_in(shelf_item.uuid for shelf_item in shelf_items),
        )
        delete_result = self._db.session.execute(delete_stmt)
        if hasattr(delete_result, "rowcount") and delete_result.rowcount:
            logger.info(f"Deleted {delete_result.rowcount} shelf items on shelf {shelf.name}")

        insert_stmt = sqlite.insert(self.model).values(  # type: ignore
            [self.to_mapping(shelf_item) for shelf_item in shelf_items]
        )
        insert_stmt = insert_stmt.on_conflict_do_nothing()
        insert_result = self._db.session.execute(insert_stmt)
        if hasattr(insert_result, "rowcount") and insert_result.rowcount:
            logger.info(f"Inserted {insert_result.rowcount} shelf items on shelf {shelf.name}")
        else:
            logger.info(f"No new shelf items inserted on shelf {shelf.name}")
