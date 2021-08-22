import logging
from typing import Dict

from src.entrypoints.jobs.base import Schedule

logger = logging.getLogger('src.entrypoints.jobs')


@Schedule.register(loop_time=15)
def refresh_shelf_books(shelf: Dict) -> None:
    ...


def main() -> None:
    try:
        Schedule.run()
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler.")


if __name__ == "__main__":
    main()
