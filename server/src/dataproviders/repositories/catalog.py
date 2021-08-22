from typing import List

from src.core.entities import Book, Catalog
from src.core.repositories import CatalogRepositoryInterface
from src.dataproviders.mixin import DbHandlerMixin
from src.dataproviders.db.model import LatestBookModel


class CatalogRepository(CatalogRepositoryInterface, DbHandlerMixin):

    def latest_books(self, catalog: Catalog) -> List[Book]:

        query = self._dbh.session.query(LatestBookModel).filter_by(catalog_id=catalog.value)

        return [
            Book(
                title=model.title,
                author=model.author,
                isbn=model.isbn,
            )
            for model in query
        ]
