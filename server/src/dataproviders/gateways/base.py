import bs4
import aiohttp
from typing import Union, Generator, AsyncIterator
from contextlib import contextmanager, asynccontextmanager


@contextmanager
def bs4_scope(markup: Union[str, bytes]) -> Generator:
    '''Parse markup to BeautifulSoup object and decompose it after use.'''
    parsed_markup = bs4.BeautifulSoup(markup, 'lxml')
    try:
        yield parsed_markup
    finally:
        parsed_markup.decompose()


@asynccontextmanager
async def aio_session(limit: int = 30) -> AsyncIterator:
    connector = aiohttp.TCPConnector(limit=limit)

    async with aiohttp.ClientSession(connector=connector, raise_for_status=True) as session:
        yield session
