import logging.config

import redis
import rq
import rq.scheduler
from src.config import Config

config = Config()

logging.config.fileConfig(config)

# Preload libraries


def run() -> None:
    connection_pool = redis.ConnectionPool(host=config.get("redis", "host"))

    connection = redis.Redis(connection_pool=connection_pool)

    queues = config.getstruct("rq", "queues")
    result_ttl = config.getint("rq", "result_ttl")
    logging_level = config.get("logger_rq", "level")

    # Release scheduler locks before starting a new worker.
    rq.scheduler.RQScheduler(
        queues=queues,
        connection=connection,
        logging_level=logging_level,
    ).release_locks()

    # Start worker with scheduler.
    rq.Worker(
        queues=queues,
        connection=connection,
        default_result_ttl=result_ttl,
    ).work(
        with_scheduler=True,
        logging_level=logging_level,
    )
