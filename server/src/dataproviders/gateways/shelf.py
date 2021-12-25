import asyncio
import logging
from typing import List, Optional
from datetime import date

import aiohttp
from src.config import Config
from src.core.entities import Book, ShelfItem, Profile, Shelf
from src.core.exceptions import BadGateway
from src.core.gateways import ShelfGatewayInterface
from src.dataproviders.gateways.base import bs4_scope, aio_session

config = Config()
logger = logging.getLogger(__name__)


class ShelfGateway(ShelfGatewayInterface):
    _url = config.get('lc', 'url')
    _library_url = config.get('lc', 'profile_library_url')
    _shelf_url: str = config.get('lc', 'profile_shelf_url')
    _items_url: str = config.get('lc', 'shelf_items_url')

    async def search(self, profile: Profile) -> List[Shelf]:
        url: str = self._library_url.format(
            profile_value=profile.value,
            profile_name=profile.name,
        )

        try:
            async with aio_session() as session:
                async with session.get(url) as response:
                    search_results = await response.read()

        except aiohttp.ClientError as e:
            raise BadGateway(f"Fetching shelves failed: {e}")

        with bs4_scope(search_results) as parsed_results:
            shelves_selector = 'ul.filtr__wrapItems input[name="shelfs[]"]'
            shelves_tags = parsed_results.select(shelves_selector)

            shelf_tasks = [
                self._set_shelf_pages(profile, Shelf(
                    name=shelf_tag['data-shelf-name'],
                    value=shelf_tag['value'],
                    profile_id=profile.profile_id,
                ))
                for shelf_tag in shelves_tags
            ]

        shelves: List[Shelf] = await asyncio.gather(*shelf_tasks)

        return shelves

    async def _set_shelf_pages(self, profile: Profile, shelf: Shelf) -> Shelf:
        async with aio_session() as session:

            url = self._shelf_url.format(
                shelf_id=shelf.value,
                profile_value=profile.value,
                profile_name=profile.name,
            )

            async with session.get(url) as response:
                content = await response.read()

                with bs4_scope(content) as shelf_page:
                    pager_tag = shelf_page.select_one(
                        'ul#buttonPaginationListP'
                        '> li.page-item:nth-last-child(2)'
                        '> a.page-link'
                    )
                    shelf.pages = int(pager_tag['data-pager-page']) if pager_tag else 1

        return shelf

    async def items(self, profile: Profile, shelf: Shelf) -> List[ShelfItem]:
        item_urls = await self._item_urls(profile, shelf)

        if not item_urls:
            logger.warning(f'No items found on shelf {shelf.name}')
            return []

        async with aio_session() as session:
            item_tasks = [self._shelf_item(session, shelf, url) for url in item_urls]

            shelf_items: List[Optional[ShelfItem]] = await asyncio.gather(*item_tasks)

        return [shelf_item for shelf_item in shelf_items if shelf_item is not None]

    async def _item_urls(self, profile: Profile, shelf: Shelf) -> List[str]:
        async with aio_session() as session:
            shelf_page_tasks = [
                self._shelf_page(session, profile, shelf, page)
                for page in range(1, shelf.pages + 1)
            ]

            contents = await asyncio.gather(*shelf_page_tasks)

        item_urls = []
        for content in contents:
            with bs4_scope(content) as markup:
                item_urls.extend([
                    f'{self._url}{link["href"]}' for link in
                    markup.select(
                        'div#booksFilteredListPaginator'
                        ' a.authorAllBooks__singleTextTitle'
                    )
                ])

        return item_urls

    async def _shelf_page(self, session: aiohttp.ClientSession, profile: Profile, shelf: Shelf, page: int) -> str:
        payload = {
            'page': page,
            'listId': 'booksFilteredList',
            'shelfs[]': shelf.value,
            'objectId': profile.value,
            'own': 0,
        }

        headers = {'X-Requested-With': 'XMLHttpRequest'}

        async with session.post(self._items_url, data=payload, headers=headers) as post:
            response = await post.json()
            content: str = response['data']['content']
            return content

    async def _shelf_item(
        self,
        session: aiohttp.ClientSession,
        shelf: Shelf,
        item_url: str,
    ) -> Optional[ShelfItem]:
        async with session.get(item_url) as response:

            content = await response.read()

            with bs4_scope(content) as item_page:
                # Get title and author.
                title = item_page.select_one('div.title-container')['data-title']

                author = item_page.select_one('span.author > a.link-name').text.strip()

                # Search for subtitle in title.
                subtitle = None
                if '. ' in title:
                    title, subtitle = title.split('. ', maxsplit=1)

                # Get details element.
                item_details = item_page.select_one('div#book-details')

                # Get original title.
                original_title_tag = item_details.select_one('dt:-soup-contains("Tytuł oryginału") + dd')
                original_title = original_title_tag.text.strip() if original_title_tag else None

                # Get pages count.
                pages_tag = item_details.select_one('dt:-soup-contains("Liczba stron") + dd')
                pages = int(pages_tag.text.strip()) if pages_tag else None

                # Get category.
                category = item_page.select_one('a.book__category').text.strip()

                # Get release date.
                release_tag = item_details.select_one('dt:-soup-contains("Data wydania") + dd')
                release = date.fromisoformat(release_tag.text.strip()) if release_tag else None

                # Get book ISBN. ISBN is not always present.
                isbn_tag = item_details.select_one('dt:-soup-contains("ISBN") + dd')

                isbn = isbn_tag.text.strip() if isbn_tag else None

                if isbn is None:
                    logger.warning(f'Skipping book "{title}" by {author} due to missing ISBN.')
                    return None

                book = Book(title=title, author=author, isbn=isbn)

                return ShelfItem(
                    book_id=book.book_id,
                    shelf_id=shelf.shelf_id,
                    title=title,
                    author=author,
                    isbn=isbn,
                    subtitle=subtitle,
                    original_title=original_title,
                    category=category,
                    pages=pages,
                    release=release,
                )
