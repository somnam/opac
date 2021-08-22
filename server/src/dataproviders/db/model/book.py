from sqlalchemy import Column
from datetime import datetime
from src.dataproviders.db.model.base import Model


class BookModel(Model):
    __tablename__ = "book"

    _pk = Column(Model.BIGINT, primary_key=True)

    book_id = Column(Model.MD5, nullable=False, index=True)

    title = Column(Model.VARCHAR(512), nullable=False)
    author = Column(Model.VARCHAR(512), nullable=False)
    isbn = Column(Model.ISBN, nullable=False, index=True)

    created_at = Column(Model.DATETIME, nullable=False, default=datetime.utcnow)


class BookMetaModel(Model):
    __tablename__ = "book_meta"

    _pk = Column(Model.BIGINT, primary_key=True)

    shelf_id = Column(Model.EXTERNAL_ID, nullable=False, index=True)
    book_id = Column(Model.MD5, nullable=False, index=True)

    subtitle = Column(Model.VARCHAR(1024), nullable=True)
    original_title = Column(Model.VARCHAR(512), nullable=True)
    category = Column(Model.VARCHAR(255), nullable=True)
    pages = Column(Model.INT, nullable=True)
    release = Column(Model.DATE, nullable=True)

    created_at = Column(Model.DATETIME, nullable=False, default=datetime.utcnow)
