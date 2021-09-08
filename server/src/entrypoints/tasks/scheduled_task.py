import logging
import logging.config

from src.core.usecases import ShelvesRefreshScheduleUseCase, ShelfItemsRefreshScheduleUseCase
from src.dataproviders.repositories import DataRepository
from src.entrypoints.tasks.base import Schedule
from src.entrypoints.tasks.task import refresh_shelves, refresh_shelf_items
from src.entrypoints.services import JobService
from src.config import Config

config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


@Schedule.register(**config.get_section('task:refresh_shelves_schedule'))
def refresh_shelves_schedule() -> None:
    refresh_schedule = ShelvesRefreshScheduleUseCase(DataRepository()).execute(
        config.getint('task:refresh_shelves_schedule', 'loop_time')
    )

    job_service = JobService()

    for schedule in refresh_schedule:
        job_service.enqueue(
            job=refresh_shelves,
            args=schedule.args,
            delay=schedule.delay,
        )


@Schedule.register(**config.get_section('task:refresh_shelf_items_schedule'))
def refresh_shelf_items_schedule() -> None:
    refresh_schedule = ShelfItemsRefreshScheduleUseCase(DataRepository()).execute(
        config.getint('task:refresh_shelf_items_schedule', 'loop_time')
    )

    job_service = JobService()

    for schedule in refresh_schedule:
        job_service.enqueue(
            job=refresh_shelf_items,
            args=schedule.args,
            delay=schedule.delay,
        )


def main() -> None:
    try:
        logger.info("Starting scheduler.")
        Schedule.run()
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler.")


if __name__ == "__main__":
    main()