from abc import abstractmethod

from src.core.gateways import DataGatewayInterface
from src.core.repositories.base import BaseRepository
from src.core.repositories.catalog import CatalogRepositoryInterface
from src.core.repositories.profile import ProfileRepositoryInterface
from src.core.repositories.shelf import ShelfRepositoryInterface
from src.core.repositories.shelf_item import ShelfItemRepositoryInterface


class DataRepositoryInterface(BaseRepository):

    @property
    @abstractmethod
    def gateway(self) -> DataGatewayInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf(self) -> ShelfRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf_item(self) -> ShelfItemRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def profile(self) -> ProfileRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def catalog(self) -> CatalogRepositoryInterface:
        raise NotImplementedError
