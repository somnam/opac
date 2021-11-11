from abc import abstractmethod
from typing import List

from src.core.entities import Book, Catalog
from src.core.repositories.base import BaseRepository


class CatalogRepositoryInterface(BaseRepository):

    @abstractmethod
    def latest_books(self, catalog: Catalog) -> List[Book]:
        raise NotImplementedError
