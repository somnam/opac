from src.core.repositories import DataRepositoryInterface

from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.repositories.shelf import ShelfRepository
from src.dataproviders.repositories.shelf_item import ShelfItemRepository
from src.dataproviders.repositories.catalog import CatalogRepository
from src.dataproviders.repositories.profile import ProfileRepository
from src.dataproviders.gateways import DataGateway


class DataRepository(DataRepositoryInterface, BaseDbRepository):

    @property
    def gateway(self) -> DataGateway:
        if not hasattr(self, "_gateway"):
            self._gateway = DataGateway()
        return self._gateway

    @property
    def profile(self) -> ProfileRepository:
        if not hasattr(self, "_profile"):
            self._profile = ProfileRepository(self._dbh)
        return self._profile

    @property
    def shelf(self) -> ShelfRepository:
        if not hasattr(self, "_shelf"):
            self._shelf = ShelfRepository(self._dbh)
        return self._shelf

    @property
    def shelf_item(self) -> ShelfItemRepository:
        if not hasattr(self, "_shelf_item"):
            self._shelf_item = ShelfItemRepository(self._dbh)
        return self._shelf_item

    @property
    def catalog(self) -> CatalogRepository:
        if not hasattr(self, "_catalog"):
            self._catalog = CatalogRepository(self._dbh)
        return self._catalog
