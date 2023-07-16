import asyncio
import logging
from typing import AsyncIterator

from src.config import Config
from src.core.entities import Profile, Shelf
from src.core.gateways import IShelfGateway
from src.dataproviders.gateways.base import BaseGateway

config = Config()
logger = logging.getLogger(__name__)


class ShelfGateway(BaseGateway, IShelfGateway):
    _library_url: str = config.get("lc", "profile_library_url")
    _shelf_url: str = config.get("lc", "profile_shelf_url")

    async def fetch_for_profile(self, profile: Profile) -> AsyncIterator[Shelf]:
        url: str = self._library_url.format(
            profile_value=profile.value,
            profile_name=profile.name,
        )

        async with self._http.session.get(url) as response:
            search_results = await response.read()

        with self.bs4_scope(search_results) as parsed_results:
            shelves_selector = 'ul.filtr__wrapItems input[name="shelfs[]"]'
            shelves_tags = parsed_results.select(shelves_selector)

            shelf_tasks = [
                self._shelf(
                    profile=profile,
                    name=shelf_tag["data-shelf-name"],
                    value=shelf_tag["value"],
                )
                for shelf_tag in shelves_tags
            ]

            for shelf_task in asyncio.as_completed(shelf_tasks):
                yield await shelf_task

    async def _shelf(self, profile: Profile, name: str, value: str) -> Shelf:
        shelf = Shelf(profile_uuid=profile.uuid, name=name, value=value)

        url = self._shelf_url.format(
            shelf_id=shelf.value,
            profile_value=profile.value,
            profile_name=profile.name,
        )

        async with self._http.session.get(url) as response:
            content = await response.read()

            with self.bs4_scope(content) as shelf_page:
                pager_tag = shelf_page.select_one("input.paginationList__input")
                if pager_tag and "data-maxpage" in pager_tag.attrs:
                    shelf.pages = int(pager_tag.attrs["data-maxpage"])

        return shelf
