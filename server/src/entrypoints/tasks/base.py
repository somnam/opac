import logging
import sched
import time
from datetime import datetime, timedelta
from threading import Thread
from typing import Callable, List

import redis
import rq
import rq.scheduler
from src.config import Config

config = Config()

logger = logging.getLogger(__name__)


class ScheduleWorker:

    def __init__(self, action: Callable, loop_time: int = 60) -> None:
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.action = action
        self.loop_time = loop_time

    def next_run_time(self) -> datetime:
        now = datetime.now().replace(microsecond=0)

        if self.loop_time == 0:
            return now

        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

        loop_delay: int = self.loop_time - ((now - midnight).seconds % self.loop_time)

        next_run_time = now + timedelta(seconds=loop_delay)

        return next_run_time

    @staticmethod
    def log_next_run_time(next_run_time: datetime) -> None:
        logger.info(f"Nearest scheduling time: {next_run_time}.")

    def periodic(self) -> None:
        run_time = self.next_run_time()

        self.scheduler.enterabs(
            time=run_time.timestamp(),
            priority=1,
            action=self.periodic,
        )

        self.action()

        self.log_next_run_time(run_time)

    def run(self) -> None:
        run_time = self.next_run_time()

        self.scheduler.enterabs(
            time=run_time.timestamp(),
            priority=1,
            action=self.periodic,
        )

        self.log_next_run_time(run_time)

        self.scheduler.run()


class Schedule:
    threads: List[Thread] = []

    @staticmethod
    def register(loop_time: int = 60) -> Callable:

        def wrapper(action: Callable) -> None:
            worker = ScheduleWorker(action, loop_time=loop_time)

            Schedule.threads.append(Thread(target=worker.run, daemon=True))

        return wrapper

    @staticmethod
    def run() -> None:
        if not Schedule.threads:
            logger.warning("No actions registered.")

        for thread in Schedule.threads:
            thread.start()

        for thread in Schedule.threads:
            thread.join()


class Worker:
    @staticmethod
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
