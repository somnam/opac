import logging
from typing import Dict, List
from urllib.parse import urlparse

import aiohttp
from src.config import Config
from src.dataproviders.gateways.base import bs4_scope
from src.core.gateways import ProfileGatewayInterface
from src.core.entities import Profile, ProfileSearchParams, ProfileSearchResult

config = Config()
logger = logging.getLogger("src.gateways")


class ProfileGateway(ProfileGatewayInterface):

    async def search(self, params: ProfileSearchParams) -> ProfileSearchResult:
        url: str = config.get('lc', 'profile_search_url')

        data: Dict[str, str] = {"listId": "searchedAccounts", **params.to_dict()}

        headers: Dict[str, str] = {"X-Requested-With": "XMLHttpRequest"}

        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.post(url, data=data, headers=headers) as response:

                    response_json = await response.json()
                    search_results = response_json["data"]["content"]
                    search_count = response_json["data"]["count"]

        except aiohttp.ClientError as e:
            logger.error(f"Fetching book urls on page failed: {e}")
            return ProfileSearchResult()

        with bs4_scope(search_results) as parsed_results:
            profiles: List[Profile] = [
                Profile(
                    name=link.text.strip(),
                    value=next(
                        (part for part in urlparse(link.get("href")).path.split('/') if part.isdigit()),
                        None,
                    ),
                )
                for link in parsed_results.select("span.user-name > a")
            ]

        return ProfileSearchResult(items=profiles, page=params.page, total=search_count)
