import logging
from contextlib import contextmanager
from sqlite3 import Connection as SQLite3Connection
from typing import Generator

from sqlalchemy import engine_from_config
from sqlalchemy.engine import Engine
from sqlalchemy.event import listens_for
from sqlalchemy.exc import (DBAPIError, InterfaceError, OperationalError,
                            SQLAlchemyError)
from sqlalchemy.orm import scoped_session, sessionmaker
from src.config import Config
from src.core.exceptions import DatabaseError
from src.dataproviders.db.model import Model

config = Config()
logger = logging.getLogger(__name__)


@listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):  # type: ignore
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()


class DbHandler:
    engine = engine_from_config(config["db:handler"])
    scoped_session = scoped_session(sessionmaker(bind=engine))

    @classmethod
    def create_schema(cls) -> None:
        Model.metadata.create_all(cls.engine, checkfirst=True)

    @contextmanager
    def session_scope(self) -> Generator:
        self.session = self.scoped_session()

        try:
            yield self.session
            self.session.commit()

        except (DBAPIError, SQLAlchemyError, InterfaceError, OperationalError) as e:
            self.session.rollback()
            raise DatabaseError() from e

        except Exception:
            self.session.rollback()
            raise

        finally:
            self.session.close()
            delattr(self, "session")
