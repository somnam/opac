import logging
from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.dialects import sqlite

from src.core.entities.book_edition import BookEdition
from src.core.entities.shelf import Shelf
from src.core.repositories.book_edition import IBookEditionRepository
from src.dataproviders.db.model.book_edition import BookEditionModel
from src.dataproviders.repositories.entity import EntityRepository

logger = logging.getLogger(__name__)


class BookEditionRepository(
    IBookEditionRepository, EntityRepository[BookEdition, BookEditionModel]
):
    def __init__(self) -> None:
        super().__init__(entity=BookEdition, model=BookEditionModel)

    def to_entity(self, model: BookEditionModel) -> BookEdition:
        return BookEdition(
            profile_uuid=model.profile_uuid,
            shelf_uuid=model.shelf_uuid,
            shelf_item_uuid=model.shelf_item_uuid,
            title=model.title,
            author=model.author,
            isbn=model.isbn,
            created_at=model.created_at,
        )

    async def sync_on_shelf(self, shelf: Shelf, book_editions: Sequence[BookEdition]) -> None:
        if not book_editions:
            return

        delete_stmt = delete(self.model).where(
            self.model.shelf_uuid == shelf.uuid,
            self.model.uuid.not_in(book_edition.uuid for book_edition in book_editions),
        )
        delete_result = self._db.session.execute(delete_stmt)
        if hasattr(delete_result, "rowcount") and delete_result.rowcount:
            logger.info(f"Deleted {delete_result.rowcount} book editions on shelf {shelf.name}")

        insert_stmt = sqlite.insert(self.model).values(  # type: ignore
            [self.to_mapping(book_edition) for book_edition in book_editions]
        )
        insert_stmt = insert_stmt.on_conflict_do_nothing()
        insert_result = self._db.session.execute(insert_stmt)
        if hasattr(insert_result, "rowcount") and insert_result.rowcount:
            logger.info(f"Inserted {insert_result.rowcount} book editions on shelf {shelf.name}")
        else:
            logger.info(f"No new book editions inserted on shelf {shelf.name}")
