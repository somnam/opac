from contextlib import contextmanager
from typing import Generator, Union

import bs4

from src.dataproviders.db import DbHandler
from src.dataproviders.http import HttpHandler


class DbHandlerMixin:
    @property
    def _db(self) -> DbHandler:
        if not hasattr(self, "_mixin_db"):
            self._mixin_db = DbHandler()
        return self._mixin_db

    @_db.setter
    def _db(self, db: DbHandler) -> None:
        self._mixin_db = db


class HttpHandlerMixin:
    @property
    def _http(self) -> HttpHandler:
        if not hasattr(self, "_mixin_http"):
            self._mixin_http = HttpHandler()
        return self._mixin_http

    @_http.setter
    def _http(self, http: HttpHandler) -> None:
        self._mixin_http = http


class Bs4Mixin:
    @contextmanager
    def bs4_scope(self, markup: Union[str, bytes]) -> Generator:
        """Parse markup to BeautifulSoup object and decompose it after use."""
        parsed_markup = bs4.BeautifulSoup(markup, "lxml")
        try:
            yield parsed_markup
        finally:
            parsed_markup.decompose()
