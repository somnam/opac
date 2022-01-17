from src.core.entities import Book, Profile, Shelf, ShelfItem
from src.core.repositories import IDataRepository
from src.dataproviders.adapters import (latest_book_from_model, profile_from_model, shelf_from_model,
                                        shelf_item_from_model)
from src.dataproviders.db import LatestBookModel, ProfileModel, ShelfItemModel, ShelfModel
from src.dataproviders.gateways import DataGateway
from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.repositories.entity import EntityRepository


class DataRepository(BaseDbRepository, IDataRepository):

    @property
    def gateway(self) -> DataGateway:
        if not hasattr(self, "_gateway"):
            self._gateway = DataGateway()
        return self._gateway

    @property
    def profile(self) -> EntityRepository:
        if not hasattr(self, "_profile"):
            self._profile = EntityRepository[Profile, ProfileModel](
                entity=Profile,
                model=ProfileModel,
                from_model=profile_from_model,
            )
            self._profile._dbh = self._dbh
        return self._profile

    @property
    def shelf(self) -> EntityRepository:
        if not hasattr(self, "_shelf"):
            self._shelf = EntityRepository[Shelf, ShelfModel](
                entity=Shelf,
                model=ShelfModel,
                from_model=shelf_from_model,
            )
            self._shelf._dbh = self._dbh
        return self._shelf

    @property
    def shelf_item(self) -> EntityRepository:
        if not hasattr(self, "_shelf_item"):
            self._shelf_item = EntityRepository[ShelfItem, ShelfItemModel](
                entity=ShelfItem,
                model=ShelfItemModel,
                from_model=shelf_item_from_model,
            )
            self._shelf_item._dbh = self._dbh
        return self._shelf_item

    @property
    def latest_book(self) -> EntityRepository:
        if not hasattr(self, "_latest_book"):
            self._latest_book = EntityRepository[Book, LatestBookModel](
                entity=Book,
                model=LatestBookModel,
                from_model=latest_book_from_model,
            )
            self._latest_book._dbh = self._dbh
        return self._latest_book
