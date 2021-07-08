from src.core.gateways import DataGatewayInterface
from src.core.repositories import (DataRepositoryInterface,
                                   JobRepositoryInterface)

from src.dataproviders.repositories.job import JobRepository
from src.dataproviders.gateways import DataGateway


class DataRepository(DataRepositoryInterface):

    @property
    def job(self) -> JobRepositoryInterface:
        if not hasattr(self, "_job"):
            self._job = JobRepository()
        return self._job

    @property
    def gateway(self) -> DataGatewayInterface:
        if not hasattr(self, "_gateway"):
            self._gateway = DataGateway()
        return self._gateway
