import logging
import aiohttp
from typing import List, Dict
from urllib.parse import urlparse
from domain.entities import (
    ProfileSearchParams,
    ProfileSearchResults,
    Profile,
    ShelvesSearchParams,
    Shelf,
)
from data.gateways.base import bs4_scope
from config import Config

config = Config()
logger = logging.getLogger("server.gateways")


class LCGateway:
    async def search_accounts(
        self,
        params: ProfileSearchParams,
    ) -> ProfileSearchResults:
        url: str = config.get('lc', 'profile_search_url')
        data: Dict[str, str] = {"listId": "searchedAccounts", **params.to_dict()}
        headers: Dict[str, str] = {"X-Requested-With": "XMLHttpRequest"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    data=data,
                    headers=headers,
                    raise_for_status=True,
                ) as response:
                    response_json = await response.json()
                    search_results = response_json["data"]["content"]
                    search_count = response_json["data"]["count"]
        except aiohttp.ClientError as e:
            logger.error(f"Fetching book urls on page failed: {e}")
            return ProfileSearchResults()

        with bs4_scope(search_results) as parsed_results:
            profiles: List[Profile] = [
                Profile(
                    name=link.text.strip(),
                    value=urlparse(link.get("href")).path,
                )
                for link in parsed_results.select("span.user-name > a")
            ]

        return ProfileSearchResults(
            items=profiles,
            page=params.page,
            total=search_count,
        )

    async def search_shelves(
        self,
        params: ShelvesSearchParams,
    ) -> List[Shelf]:
        profile = params.profile
        url: str = config.get('lc', 'profile_library_url').format(
            profile_id=profile.value
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, raise_for_status=True) as response:
                    search_results = await response.read()
        except aiohttp.ClientError as e:
            logger.error(f"Fetching shelves failed: {e}")
            return []

        with bs4_scope(search_results) as parsed_results:
            shelves_selector = 'ul.filtr__wrapItems input[name="shelfs[]"]'
            shelves_tags = parsed_results.select(shelves_selector)

            shelves: List[Shelf] = [
                Shelf(
                    name=shelf_tag['data-shelf-name'],
                    value=shelf_tag['value'],
                )
                for shelf_tag in shelves_tags
            ]

        return shelves
