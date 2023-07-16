from abc import abstractmethod

from src.core.repositories.base import IRepository
from src.core.repositories.book_edition import IBookEditionRepository
from src.core.repositories.entity import IEntityRepository
from src.core.repositories.latest_book import ILatestBookRepository
from src.core.repositories.shelf import IShelfRepository
from src.core.repositories.shelf_item import IShelfItemRepository


class IDataRepository(IRepository):
    @property
    @abstractmethod
    def profile(self) -> IEntityRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf(self) -> IShelfRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def shelf_item(self) -> IShelfItemRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def book_edition(self) -> IBookEditionRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def latest_book(self) -> ILatestBookRepository:
        raise NotImplementedError
