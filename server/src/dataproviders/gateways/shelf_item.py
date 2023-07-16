import asyncio
import logging
from typing import AsyncIterator, Dict, Union

from src.config import Config
from src.core.entities import Profile, Shelf, ShelfItem
from src.core.entities.book_buy import BookBuyUrl
from src.core.entities.book_edition import BookEdition
from src.core.gateways import IShelfItemGateway
from src.dataproviders.gateways.base import BaseGateway

config = Config()
logger = logging.getLogger(__name__)


class ShelfItemGateway(BaseGateway, IShelfItemGateway):
    _items_url: str = config.get("lc", "shelf_items_url")
    _headers: Dict[str, str] = {"X-Requested-With": "XMLHttpRequest"}

    async def fetch_for_profile_and_shelf(
        self, profile: Profile, shelf: Shelf
    ) -> AsyncIterator[ShelfItem]:
        pages = range(1, shelf.pages + 1)
        page_tasks = [self._shelf_page(profile, shelf, page) for page in pages]

        for page_task in asyncio.as_completed(page_tasks):
            content = await page_task

            with self.bs4_scope(content) as markup:
                book_element_selector = "div#booksFilteredListPaginator div.authorAllBooks__single"
                book_title_selector = "a.authorAllBooks__singleTextTitle"
                book_author_selector = "div.authorAllBooks__singleTextAuthor a"
                book_button_selector = "button.openBBMenu"
                for book_element_tag in markup.select(book_element_selector):
                    value = book_element_tag.get("id", "").replace("listBookElement", "")
                    if not (value and value.isdigit()):
                        continue

                    title_tag = book_element_tag.select_one(book_title_selector)
                    author_tag = book_element_tag.select_one(book_author_selector)
                    title_value = title_tag.text.strip()
                    author_value = author_tag.text.strip()

                    shelf_item = ShelfItem(
                        profile_uuid=profile.uuid,
                        shelf_uuid=shelf.uuid,
                        title=title_value,
                        author=author_value,
                        value=value,
                    )

                    button_tag = book_element_tag.select_one(book_button_selector)
                    if button_tag and button_tag.attrs.get("data-bb-url"):
                        book_buy_url = BookBuyUrl(uri=button_tag.attrs["data-bb-url"])
                        shelf_item.book_editions = [
                            BookEdition(
                                profile_uuid=profile.uuid,
                                shelf_uuid=shelf.uuid,
                                shelf_item_uuid=shelf_item.uuid,
                                title=shelf_item.title,
                                author=shelf_item.author,
                                isbn=isbn,
                            )
                            for isbn in book_buy_url.isbn_list
                        ]

                    yield shelf_item

    async def _shelf_page(self, profile: Profile, shelf: Shelf, page: int) -> str:
        payload: Dict[str, Union[str, int]] = {
            "page": page,
            "listId": "booksFilteredList",
            "shelfs[]": shelf.value,
            "objectId": profile.value,
            "own": 0,
        }

        logger.info(f"Fetch shelf {shelf.name} page {page} on profile {profile.name}")

        async with self._http.session.post(
            self._items_url,
            data=payload,
            headers=self._headers,
        ) as post:
            response = await post.json()
            content: str = response["data"]["content"]
            return content
