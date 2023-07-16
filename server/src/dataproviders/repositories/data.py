from src.core.repositories import IDataRepository
from src.dataproviders.repositories.base import BaseRepository
from src.dataproviders.repositories.book_edition import BookEditionRepository
from src.dataproviders.repositories.latest_book import LatestBookRepository
from src.dataproviders.repositories.profile import ProfileRepository
from src.dataproviders.repositories.shelf import ShelfRepository
from src.dataproviders.repositories.shelf_item import ShelfItemRepository


class DataRepository(BaseRepository, IDataRepository):
    @property
    def profile(self) -> ProfileRepository:
        if not hasattr(self, "_profile"):
            self._profile = ProfileRepository()
            self._profile._db = self._db
        return self._profile

    @property
    def shelf(self) -> ShelfRepository:
        if not hasattr(self, "_shelf"):
            self._shelf = ShelfRepository()
            self._shelf._db = self._db
        return self._shelf

    @property
    def shelf_item(self) -> ShelfItemRepository:
        if not hasattr(self, "_shelf_item"):
            self._shelf_item = ShelfItemRepository()
            self._shelf_item._db = self._db
        return self._shelf_item

    @property
    def book_edition(self) -> BookEditionRepository:
        if not hasattr(self, "_book_edition"):
            self._book_edition = BookEditionRepository()
            self._book_edition._db = self._db
        return self._book_edition

    @property
    def latest_book(self) -> LatestBookRepository:
        if not hasattr(self, "_latest_book"):
            self._latest_book = LatestBookRepository()
            self._latest_book._db = self._db
        return self._latest_book
