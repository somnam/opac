from src.dataproviders.db.handler import DbHandler


def run() -> None:
    DbHandler.create_schema()
