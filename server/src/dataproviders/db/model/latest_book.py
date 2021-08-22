from sqlalchemy import Column
from datetime import datetime
from src.dataproviders.db.model.base import Model


class LatestBookModel(Model):
    __tablename__ = "latest_book"

    _pk = Column(Model.BIGINT, primary_key=True)

    catalog_id = Column(Model.EXTERNAL_ID, nullable=False, index=True)
    book_id = Column(Model.MD5, nullable=False, index=True)
    url_id = Column(Model.MD5, nullable=False, index=True)

    title = Column(Model.VARCHAR(512), nullable=False)
    author = Column(Model.VARCHAR(512), nullable=False)
    isbn = Column(Model.ISBN, nullable=False, index=True)

    created_at = Column(Model.DATETIME, nullable=False, default=datetime.utcnow)
