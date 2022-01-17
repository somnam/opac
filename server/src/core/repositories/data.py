from abc import abstractmethod

from src.core.gateways import IDataGateway
from src.core.repositories.base import IRepository
from src.core.repositories.entity import IEntityRepository


class IDataRepository(IRepository):

    @property
    @abstractmethod
    def gateway(self) -> IDataGateway:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf(self) -> IEntityRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf_item(self) -> IEntityRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def profile(self) -> IEntityRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def latest_book(self) -> IEntityRepository:
        raise NotImplementedError
