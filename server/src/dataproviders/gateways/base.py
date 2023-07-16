from typing import AsyncContextManager

from src.dataproviders.mixin import Bs4Mixin, HttpHandlerMixin


class BaseGateway(HttpHandlerMixin, Bs4Mixin):
    def context(self) -> AsyncContextManager:
        return self._http.session_scope()
