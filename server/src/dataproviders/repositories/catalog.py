from typing import List

from src.core.entities import Book, Catalog
from src.core.repositories import CatalogRepositoryInterface
from src.dataproviders.db.model import LatestBookModel
from src.dataproviders.repositories.base import BaseDbRepository


class CatalogRepository(CatalogRepositoryInterface, BaseDbRepository):

    def latest_books(self, catalog: Catalog) -> List[Book]:

        query = self._dbh.session.query(LatestBookModel).filter_by(catalog_id=catalog.catalog_id)

        return [
            Book(
                title=model.title,
                author=model.author,
                isbn=model.isbn,
            )
            for model in query
        ]
