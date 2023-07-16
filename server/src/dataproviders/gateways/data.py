from src.core.gateways.data import IDataGateway
from src.dataproviders.gateways.base import BaseGateway
from src.dataproviders.gateways.book_edition import BookEditionGateway
from src.dataproviders.gateways.profile import ProfileGateway
from src.dataproviders.gateways.shelf import ShelfGateway
from src.dataproviders.gateways.shelf_item import ShelfItemGateway


class DataGateway(BaseGateway, IDataGateway):
    @property
    def profile(self) -> ProfileGateway:
        if not hasattr(self, "_profile"):
            self._profile = ProfileGateway()
            self._profile._http = self._http
        return self._profile

    @property
    def shelf(self) -> ShelfGateway:
        if not hasattr(self, "_shelf"):
            self._shelf = ShelfGateway()
            self._shelf._http = self._http
        return self._shelf

    @property
    def shelf_item(self) -> ShelfItemGateway:
        if not hasattr(self, "_shelf_item"):
            self._shelf_item = ShelfItemGateway()
            self._shelf_item._http = self._http
        return self._shelf_item

    @property
    def book_edition(self) -> BookEditionGateway:
        if not hasattr(self, "_book_edition"):
            self._book_edition = BookEditionGateway()
            self._book_edition._http = self._http
        return self._book_edition
