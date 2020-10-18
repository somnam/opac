import asyncio
from typing import List
from domain.entities import Activity, SearchResults
from config import Config

config = Config()


class GetActivitiesUseCase:
    async def execute(self) -> SearchResults:
        await asyncio.sleep(0)

        activities: List[Activity] = [Activity(**entry) for entry in
                                      config.getstruct('activities', 'list')]
        return SearchResults(items=activities)
