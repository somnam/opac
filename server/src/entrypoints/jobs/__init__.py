from src.entrypoints.jobs.base import job_on_success
from src.entrypoints.jobs.search_latest_books import search_latest_books


__all__ = [
    "search_latest_books",
    "job_on_success",
]
