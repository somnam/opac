from typing import List, Optional

from sqlalchemy import select

from src.core.entities import Catalog, LatestBook, Shelf
from src.core.repositories.latest_book import ILatestBookRepository
from src.dataproviders.db.model.latest_book import LatestBookModel
from src.dataproviders.repositories.entity import EntityRepository


class LatestBookRepository(ILatestBookRepository, EntityRepository[LatestBook, LatestBookModel]):
    def __init__(self) -> None:
        super().__init__(entity=LatestBook, model=LatestBookModel)

    def to_entity(self, model: LatestBookModel) -> LatestBook:
        return LatestBook(
            catalog_uuid=model.catalog_uuid,
            title=model.title,
            author=model.author,
            isbn=model.isbn,
            created_at=model.created_at,
        )

    async def search_in_catalog_by_shelves(
        self,
        catalog: Catalog,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]],
    ) -> List[LatestBook]:
        # TODO: filter by included / excluded Shelves
        stmt = select(self.model).where(self.model.catalog_uuid == catalog.uuid)
        models = self._db.session.scalars(stmt)

        return [self.to_entity(model) for model in models]
