from typing import Dict, List
from urllib.parse import urlparse

from src.config import Config
from src.core.entities import Profile, ProfileSearchParams, ProfileSearchResult
from src.core.gateways import IProfileGateway
from src.dataproviders.gateways.base import BaseGateway

config = Config()


class ProfileGateway(BaseGateway, IProfileGateway):
    _url: str = config.get("lc", "profile_search_url")

    async def search(self, params: ProfileSearchParams) -> ProfileSearchResult:
        data: Dict[str, str] = {"listId": "searchedAccounts", **params.dict()}

        headers: Dict[str, str] = {"X-Requested-With": "XMLHttpRequest"}

        async with self._http.session.post(self._url, data=data, headers=headers) as response:
            response_json = await response.json()
            search_results = response_json["data"]["content"]
            search_count = response_json["data"]["count"]

        with self.bs4_scope(search_results) as parsed_results:
            profiles: List[Profile] = []

            for link in parsed_results.select("span.user-name > a"):
                parts = urlparse(link.get("href")).path.split("/")
                value = next((part for part in parts if part.isdigit()), None)
                if value is None:
                    continue

                profiles.append(Profile(name=link.text.strip(), value=value))

        return ProfileSearchResult(items=profiles, page=params.page, total=search_count)
