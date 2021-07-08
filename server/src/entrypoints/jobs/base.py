import logging
from typing import Any

import redis
import rq
from src.dataproviders.gateways import DataGateway

logger = logging.getLogger('src.entrypoints.jobs')


def job_on_success(job: rq.job.Job, connection: redis.Redis, result: Any) -> None:

    job_id = job.get_id()

    client_id: int = job.meta.get("client_id", 0)

    job.meta["progress"] = 100

    job.save()

    if client_id:
        logger.warn(f'Pushing job {job_id} result to client {client_id}.')

        DataGateway().client.push(client_id=client_id, job_id=job_id, operation="job-success")
