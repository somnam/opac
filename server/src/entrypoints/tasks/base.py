import logging
import sched
import time
from datetime import datetime, timedelta
from typing import List, Callable
from threading import Thread

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
