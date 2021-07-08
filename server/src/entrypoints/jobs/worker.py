import rq
import redis

from src.config import Config

config = Config()

# Preload libraries


def run() -> None:
    connection_pool = redis.ConnectionPool(host=config.get("redis", "host"))

    connection = redis.Redis(connection_pool=connection_pool)

    with rq.Connection(connection):
        queues = config.getstruct("rq", "queues")

        rq.Worker(queues=queues).work()
