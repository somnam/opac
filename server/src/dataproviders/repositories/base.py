from typing import Optional
from src.dataproviders.db import DbHandler
from src.dataproviders.mixin import DbHandlerMixin


class BaseDbRepository(DbHandlerMixin):

    def __init__(self, dbh: Optional[DbHandler] = None) -> None:
        if dbh is not None:
            self._dbh = dbh
