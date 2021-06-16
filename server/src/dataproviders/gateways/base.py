import bs4
from typing import Union, Generator
from contextlib import contextmanager


@contextmanager
def bs4_scope(markup: Union[str, bytes]) -> Generator:
    '''Parse markup to BeautifulSoup object and decompose it after use.'''
    parsed_markup = bs4.BeautifulSoup(markup, 'lxml')
    try:
        yield parsed_markup
    finally:
        parsed_markup.decompose()
