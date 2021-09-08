import logging
import logging.config

from datetime import timedelta
from typing import Any, Callable, Optional

import redis
import rq
from src.config import Config
from src.dataproviders.gateways import DataGateway


config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


class JobService:
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
        delay: Optional[int] = None,
        **options: Optional[Any],
    ) -> int:

        if delay:
            queued_job = self.queue.enqueue_in(
                timedelta(seconds=delay),
                job,
                meta=meta,
                args=args,
                kwargs=kwargs,
                **options,
            )

        else:
            queued_job = self.queue.enqueue(
                job,
                meta=meta,
                args=args,
                kwargs=kwargs,
                **options,
            )

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

    @staticmethod
    def push_result(job: rq.job.Job, connection: redis.Redis, result: Any) -> None:

        job.meta["progress"] = 100

        job.save()

        client_id: int = job.meta.get("client_id", 0)

        if client_id:
            logger.info(f'Pushing job {job.get_id()} result to client {client_id}.')

            DataGateway().client.push(client_id=client_id, job_id=job.get_id(), operation="job-result")
