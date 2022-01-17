from sqlalchemy import Column
from datetime import datetime
from src.dataproviders.db.model.base import Model


class LatestBookModel(Model):
    __tablename__ = "latest_book"

    _pk = Column(Model.BIGINT, primary_key=True)

    uuid = Column(Model.UUID, nullable=False, index=True)
    catalog_uuid = Column(Model.UUID, nullable=False, index=True)

    title = Column(Model.VARCHAR(512), nullable=False)
    author = Column(Model.VARCHAR(512), nullable=False)
    isbn = Column(Model.ISBN, nullable=False, index=True)

    created_at = Column(Model.DATETIME, nullable=False, default=datetime.utcnow)
