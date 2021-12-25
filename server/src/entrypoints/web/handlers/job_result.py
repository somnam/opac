import logging
from typing import Any, Dict, Tuple

import tornado.web

from src.entrypoints.exceptions import ClientNotFound, JobNotFound
from src.entrypoints.services import JobService
from src.entrypoints.web.handlers.websocket import WebSocketHandler
from src.entrypoints.web.mixin import ErrorHandlerMixin, JsonSchemaMixin

logger = logging.getLogger(__name__)


class JobResultHandler(tornado.web.RequestHandler, JsonSchemaMixin, ErrorHandlerMixin):
    @classmethod
    def route(cls, **kwargs: Dict) -> Tuple[str, Any, Dict[str, Any]]:
        # route / handler / kwargs
        return (r"/client/(?P<client_id>\w+)/job-result", cls, kwargs)

    def initialize(self) -> None:
        self.job_service = JobService()

    def post(self, *args: Any, **kwargs: Any) -> None:

        with self.handle_error():

            client_id = kwargs["client_id"]

            logger.info(f"Endpoint called with client_id {client_id}.")

            client = WebSocketHandler.clients.get(client_id)

            if not client:
                raise ClientNotFound(f"Client with id {client_id} not found.")

            payload = self.decode_message(self.request.body)

            job_id = payload["job_id"]

            if not self.job_service.exists(job_id):
                raise JobNotFound(f"Job with id {job_id} not found.")

            operation = self.job_service.operation(job_id)

            finished = self.job_service.finished(job_id)

            result = self.job_service.result(job_id) if finished else None

            logger.info(f"Job {job_id} result: {result}")

            response = {
                "operation": operation,
                "payload": {"finished": finished, "result": result},
            }

            client.write_message(self.encode_message(response))
