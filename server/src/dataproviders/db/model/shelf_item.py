from sqlalchemy import Column
from datetime import datetime
from src.dataproviders.db.model.base import Model


class ShelfItemModel(Model):
    __tablename__ = "shelf_item"

    _pk = Column(Model.BIGINT, primary_key=True)

    uuid = Column(Model.UUID, nullable=False, index=True)
    book_uuid = Column(Model.UUID, nullable=False, index=True)
    shelf_uuid = Column(Model.UUID, nullable=False, index=True)

    title = Column(Model.VARCHAR(512), nullable=False)
    author = Column(Model.VARCHAR(512), nullable=False)
    isbn = Column(Model.ISBN, nullable=False, index=True)

    subtitle = Column(Model.VARCHAR(1024), nullable=True)
    original_title = Column(Model.VARCHAR(512), nullable=True)
    category = Column(Model.VARCHAR(255), nullable=True)
    pages = Column(Model.INT, nullable=True)
    release = Column(Model.DATE, nullable=True)

    created_at = Column(Model.DATETIME, nullable=False, default=datetime.utcnow)
