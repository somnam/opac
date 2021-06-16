import logging
from typing import List

import aiohttp
from config import Config
from src.dataproviders.gateways.base import bs4_scope
from src.core.gateways import ShelvesGatewayInterface
from src.core.entities import Shelf, ShelvesSearchParams

config = Config()
logger = logging.getLogger("src.gateways")


class ShelvesGateway(ShelvesGatewayInterface):

    async def search(self, params: ShelvesSearchParams) -> List[Shelf]:
        url: str = config.get('lc', 'profile_library_url').format(
            profile_id=params.profile.value
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
                Shelf(name=shelf_tag['data-shelf-name'],
                      value=shelf_tag['value'])
                for shelf_tag in shelves_tags
            ]

        return shelves
