from src.core.gateways import DataGatewayInterface
from src.core.repositories import (DataRepositoryInterface,
                                   JobRepositoryInterface,
                                   ShelfRepositoryInterface,
                                   ShelfItemRepositoryInterface,
                                   CatalogRepositoryInterface)

from src.dataproviders.repositories.job import JobRepository
from src.dataproviders.repositories.shelf import ShelfRepository
from src.dataproviders.repositories.shelf_item import ShelItemfRepository
from src.dataproviders.repositories.catalog import CatalogRepository
from src.dataproviders.gateways import DataGateway


class DataRepository(DataRepositoryInterface):

    @property
    def gateway(self) -> DataGatewayInterface:
        if not hasattr(self, "_gateway"):
            self._gateway = DataGateway()
        return self._gateway

    @property
    def job(self) -> JobRepositoryInterface:
        if not hasattr(self, "_job"):
            self._job = JobRepository()
        return self._job

    @property
    def shelf(self) -> ShelfRepositoryInterface:
        if not hasattr(self, "_shelf"):
            self._shelf = ShelfRepository()
        return self._shelf

    @property
    def shelf_item(self) -> ShelfItemRepositoryInterface:
        if not hasattr(self, "_shelf_item"):
            self._shelf_item = ShelItemfRepository()
        return self._shelf_item

    @property
    def catalog(self) -> CatalogRepositoryInterface:
        if not hasattr(self, "_catalog"):
            self._catalog = CatalogRepository()
        return self._catalog
