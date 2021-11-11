import logging
from typing import Any, Dict, Tuple

import tornado.web
from src.entrypoints.exceptions import JobNOtFound, MessageDecodeError
from src.entrypoints.services import JobService
from src.entrypoints.web.handlers.websocket import WebSocketHandler
from src.entrypoints.web.mixin import JsonSchemaMixin

logger = logging.getLogger(__name__)


class JobResultHandler(tornado.web.RequestHandler, JsonSchemaMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/client/(?P<client_id>\w+)/job-result", cls, kwargs)

    def initialize(self) -> None:
        self.job_service = JobService()

    def post(self, *args: Any, **kwargs: Any) -> None:
        client_id = kwargs["client_id"]

        logger.info(f"Endpoint called with client_id {client_id}.")

        client = WebSocketHandler.clients.get(client_id)

        if not client:
            logger.error(f"Client with id {client_id} not found.")
            return

        try:
            payload = self.decode_message(self.request.body)
        except MessageDecodeError as e:
            logger.error(f"Error decoding message: {e!s}")
            return

        job_id = payload["job_id"]

        if not self.job_service.exists(job_id):
            raise JobNOtFound()

        operation = self.job_service.operation(job_id)

        finished = self.job_service.finished(job_id)

        result = self.job_service.result(job_id) if finished else None

        logger.info(f"Job {job_id} result: {result}")

        response = {"operation": operation, "payload": {"finished": finished, "result": result}}

        client.write_message(self.encode_message(response))
