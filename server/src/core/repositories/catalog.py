from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Book, Catalog


class CatalogRepositoryInterface(ABC):

    @abstractmethod
    def latest_books(self, catalog: Catalog) -> List[Book]:
        raise NotImplementedError
