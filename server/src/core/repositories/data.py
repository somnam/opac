from abc import ABC, abstractmethod

from src.core.repositories.job import JobRepositoryInterface
from src.core.repositories.shelf import ShelfRepositoryInterface
from src.core.repositories.catalog import CatalogRepositoryInterface
from src.core.gateways import DataGatewayInterface


class DataRepositoryInterface(ABC):

    @property
    @abstractmethod
    def gateway(self) -> DataGatewayInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def job(self) -> JobRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf(self) -> ShelfRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def catalog(self) -> CatalogRepositoryInterface:
        raise NotImplementedError
