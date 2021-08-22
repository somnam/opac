from src.dataproviders.db.model.base import Model
from src.dataproviders.db.model.book import BookModel, BookMetaModel
from src.dataproviders.db.model.latest_book import LatestBookModel

__all__ = [
    "Model",
    "BookModel",
    "BookMetaModel",
    "LatestBookModel"
]
