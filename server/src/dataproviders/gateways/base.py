from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Generator, Union

import aiohttp
import bs4

from src.config import Config

config = Config()


@contextmanager
def bs4_scope(markup: Union[str, bytes]) -> Generator:
    '''Parse markup to BeautifulSoup object and decompose it after use.'''
    parsed_markup = bs4.BeautifulSoup(markup, 'lxml')
    try:
        yield parsed_markup
    finally:
        parsed_markup.decompose()


@asynccontextmanager
async def aio_session(limit: int = config.getint('gateway', 'connections')) -> AsyncIterator:
    connector = aiohttp.TCPConnector(limit=limit)

    async with aiohttp.ClientSession(connector=connector, raise_for_status=True) as session:
        yield session
