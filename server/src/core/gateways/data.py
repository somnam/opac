from abc import abstractmethod

from src.core.gateways.base import IGateway
from src.core.gateways.book_edition import IBookEditionGateway
from src.core.gateways.profile import IProfileGateway
from src.core.gateways.shelf import IShelfGateway
from src.core.gateways.shelf_item import IShelfItemGateway


class IDataGateway(IGateway):
    @property
    @abstractmethod
    def profile(self) -> IProfileGateway:
        ...

    @property
    @abstractmethod
    def shelf(self) -> IShelfGateway:
        ...

    @property
    @abstractmethod
    def shelf_item(self) -> IShelfItemGateway:
        ...

    @property
    @abstractmethod
    def book_edition(self) -> IBookEditionGateway:
        ...
