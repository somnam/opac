import logging
from typing import Any, Callable, Optional

import redis
import rq
from src.config import Config
from src.core.repositories import JobRepositoryInterface

config = Config()

logger = logging.getLogger('src.dataproviders.repositories')


class JobRepository(JobRepositoryInterface):
    connection_pool = redis.ConnectionPool(host=config.get("redis", "host"))
    connection = redis.Redis(connection_pool=connection_pool)
    serializer = rq.serializers.DefaultSerializer

    _sleep_time = 1

    def __init__(self) -> None:

        self.queue = rq.Queue(connection=self.connection)

    def exists(self, job_id: str) -> bool:
        exists: bool = rq.job.Job.exists(job_id, self.connection)
        return exists

    def enqueue(
        self,
        job: Callable,
        meta: Optional[dict] = None,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
        **options: Optional[Any],
    ) -> int:

        queued_job = self.queue.enqueue(job, meta=meta, args=args, kwargs=kwargs, **options)

        job_id: int = queued_job.get_id()

        return job_id

    def finished(self, job_id: int) -> bool:
        serialized = self._get_serialized(job_id, "meta")

        meta = self.serializer.loads(serialized) if serialized else {}

        progress: int = meta.get("progress", 0)

        return progress == 100

    def result(self, job_id: int) -> Any:
        serialized = self._get_serialized(job_id, "result")

        return self.serializer.loads(serialized) if serialized else None

    def operation(self, job_id: int) -> Optional[str]:
        serialized = self._get_serialized(job_id, "meta")

        meta = self.serializer.loads(serialized) if serialized else {}

        operation: Optional[str] = meta.get("operation")

        return operation

    def _get_serialized(self, job_id: int, field: str) -> Any:
        job_key = rq.job.Job.key_for(job_id)

        return self.connection.hget(job_key, field)
