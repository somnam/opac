import logging
from typing import List

from src.config import Config
from src.core.entities import ShelfItem
from src.core.entities.book_buy import BookBuyUrl
from src.core.entities.book_edition import BookEdition
from src.core.gateways.book_edition import IBookEditionGateway
from src.dataproviders.gateways.base import BaseGateway

config = Config()
logger = logging.getLogger(__name__)


class BookEditionGateway(BaseGateway, IBookEditionGateway):
    _book_editions_url: str = config.get("lc", "book_editions_url")

    async def fetch_for_shelf_item(self, shelf_item: ShelfItem) -> List[BookEdition]:
        url: str = self._book_editions_url.format(
            shelf_item_value=shelf_item.value,
        )

        async with self._http.session.get(url) as response:
            shelf_item_result = await response.read()

        with self.bs4_scope(shelf_item_result) as markup:
            book_element_selector = "div#editionsList div.authorAllBooks__single"
            book_button_selector = f"{book_element_selector} button.openBBMenu"
            button_tag = markup.select_one(book_button_selector)

            if button_tag and button_tag.attrs.get("data-bb-url"):
                book_buy_url = BookBuyUrl(uri=button_tag.attrs["data-bb-url"])
                book_editions = [
                    BookEdition(
                        profile_uuid=shelf_item.profile_uuid,
                        shelf_uuid=shelf_item.shelf_uuid,
                        shelf_item_uuid=shelf_item.uuid,
                        title=shelf_item.title,
                        author=shelf_item.author,
                        isbn=isbn,
                    )
                    for isbn in book_buy_url.isbn_list
                ]
            else:
                book_editions = []

        return book_editions
