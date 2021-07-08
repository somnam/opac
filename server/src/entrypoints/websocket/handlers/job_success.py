import logging
from typing import Dict

from src.dataproviders.repositories import DataRepository
from src.entrypoints.websocket.exceptions import JobNOtFound
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger('src.entrypoints.websocket')


class JobSuccessHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'job-success'

    def execute(self, payload: dict) -> Dict[str, int]:
        job_id = payload["job_id"]

        repository = DataRepository()

        if not repository.job.exists(job_id):
            raise JobNOtFound()

        operation = repository.job.operation(job_id)

        finished = repository.job.finished(job_id)

        result = repository.job.result(job_id) if finished else None

        return {"operation": operation, "payload": {"finished": finished, "result": result}}
