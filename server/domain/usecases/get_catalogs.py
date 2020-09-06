import asyncio
from typing import List
from domain.entities import Catalog
from config import Config

config = Config()


class GetCatalogsUseCase:
    async def execute(self) -> List[Catalog]:
        await asyncio.sleep(0)

        catalogs: List[Catalog] = [Catalog(**entry) for entry in
                                   config.getstruct('catalogs', 'list')]
        return catalogs
