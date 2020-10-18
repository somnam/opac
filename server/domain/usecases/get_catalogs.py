import asyncio
from typing import List
from domain.entities import Catalog, SearchResults
from config import Config

config = Config()


class GetCatalogsUseCase:
    async def execute(self) -> SearchResults:
        await asyncio.sleep(0)

        catalogs: List[Catalog] = [Catalog(**entry) for entry in
                                   config.getstruct('catalogs', 'list')]
        return SearchResults(items=catalogs)
