from typing import TypeVar

from src.dataproviders.db import Model

__all__ = [
    "TModel"
]

TModel = TypeVar("TModel", bound=Model)
