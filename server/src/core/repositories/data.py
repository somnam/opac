from abc import ABC, abstractmethod

from src.core.repositories.job import JobRepositoryInterface
from src.core.gateways import DataGatewayInterface


class DataRepositoryInterface(ABC):

    @property
    @abstractmethod
    def job(self) -> JobRepositoryInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def gateway(self) -> DataGatewayInterface:
        raise NotImplementedError
