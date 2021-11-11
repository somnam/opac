import inspect
import logging
import logging.config
import uuid
from datetime import timedelta
from typing import Any, Callable, Generator, Optional
from contextlib import contextmanager

import redis
import rq
from rq.job import JobStatus
from src.config import Config
from src.dataproviders.gateways import DataGateway

config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


class JobService:
    _connection_pool = redis.ConnectionPool(host=config.get("redis", "host"))
    _connection = redis.Redis(connection_pool=_connection_pool)
    _serializer = rq.serializers.DefaultSerializer

    def __init__(self) -> None:
        self._queue = rq.Queue(connection=self._connection)
        self._one_at_a_time = False

    @contextmanager
    def one_at_a_time(self) -> Generator:
        try:
            self._one_at_a_time = True
            yield

        finally:
            self._one_at_a_time = False

    def exists(self, job_id: str) -> bool:
        exists: bool = rq.job.Job.exists(job_id, self._connection)
        return exists

    def enqueue(
        self,
        job: Callable,
        meta: Optional[dict] = None,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
        delay: Optional[int] = None,
        **options: Optional[Any],
    ) -> str:

        job_id = JobUtil.job_id(job, args, kwargs)

        if self._one_at_a_time and self.exists(job_id):
            logger.warn(f"Job with (ID) {job_id} already exists.")
            return job_id

        options.update({
            "job_id": job_id,
            "meta": meta,
            "args": args,
            "kwargs": kwargs,
        })

        if delay:
            self._queue.enqueue_in(timedelta(seconds=delay), job, **options)

        else:
            self._queue.enqueue(job, **options)

        return job_id

    def finished(self, job_id: int) -> bool:
        serialized = self._get_serialized(job_id, "status")

        status = serialized.decode('utf-8') if isinstance(serialized, bytes) else serialized

        finished: bool = status == JobStatus.FINISHED

        return finished

    def result(self, job_id: int) -> Any:
        serialized = self._get_serialized(job_id, "result")

        return self._serializer.loads(serialized) if serialized else None

    def operation(self, job_id: int) -> Optional[str]:
        serialized = self._get_serialized(job_id, "meta")

        meta = self._serializer.loads(serialized) if serialized else {}

        operation: Optional[str] = meta.get("operation")

        return operation

    def _get_serialized(self, job_id: int, field: str) -> Any:
        job_key = rq.job.Job.key_for(job_id)

        return self._connection.hget(job_key, field)

    @staticmethod
    def push_result(job: rq.job.Job, connection: redis.Redis, result: Any) -> None:
        client_id: str = job.meta.get("client_id", "")

        if client_id:
            logger.info(f'Pushing job {job.get_id()} result to client {client_id}.')

            DataGateway().client.push(client_id=client_id, job_id=job.get_id(), operation="job-result")


class JobUtil:

    @classmethod
    def job_id(cls, job: Callable, args: Optional[list], kwargs: Optional[dict]) -> str:
        job_name = cls.job_name(job)

        args_repr = ''
        if args:
            args_repr = ', '.join((repr(arg) for arg in args))

        kwargs_repr = ''
        if kwargs:
            kwargs_repr = ', '.join(sorted((f'{key}={repr(value)}' for key, value in kwargs.items())))

        return str(uuid.uuid5(
            namespace=uuid.NAMESPACE_DNS,
            name="+".join((job_name, args_repr, kwargs_repr))
        ))

    @classmethod
    def job_name(cls, job: Callable) -> str:
        if inspect.ismethod(job):
            job_name = job.__name__

        elif inspect.isfunction(job) or inspect.isbuiltin(job):
            job_name = f'{job.__module__}.{job.__qualname__}'

        elif not inspect.isclass(job) and hasattr(job, '__call__'):
            job_name = '__call__'

        else:
            job_name = str(job)

        return job_name
