from abc import ABC, abstractmethod

from src.core.gateways.shelf import IShelfGateway
from src.core.gateways.profile import IProfileGateway
from src.core.gateways.client import IClientGateway


class IDataGateway(ABC):

    @property
    @abstractmethod
    def shelf(self) -> IShelfGateway:
        raise NotImplementedError

    @property
    @abstractmethod
    def profile(self) -> IProfileGateway:
        raise NotImplementedError

    @property
    def client(self) -> IClientGateway:
        raise NotImplementedError
