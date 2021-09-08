import logging
from typing import Dict

from src.entrypoints.websocket.exceptions import JobNOtFound
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.entrypoints.services import JobService

logger = logging.getLogger(__name__)


class JobResultHandler(HandlerInterface):
    def __init__(self) -> None:
        self._job_service = JobService()

    @classmethod
    def operation(cls) -> str:
        return 'job-result'

    def execute(self, payload: dict) -> Dict[str, Dict]:
        job_id = payload["job_id"]

        if not self._job_service.exists(job_id):
            raise JobNOtFound()

        operation = self._job_service.operation(job_id)

        finished = self._job_service.finished(job_id)

        result = self._job_service.result(job_id) if finished else None

        logger.info(f"Job {job_id} result: {result}")

        return {"operation": operation, "payload": {"finished": finished, "result": result}}
