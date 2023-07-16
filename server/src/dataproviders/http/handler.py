import logging
from contextlib import asynccontextmanager
from functools import cached_property
from types import SimpleNamespace
from typing import AsyncGenerator

import aiohttp
from aiohttp.tracing import (
    TraceConnectionCreateStartParams,
    TraceRequestEndParams,
    TraceRequestStartParams,
)

from src.config import Config
from src.core.exceptions import BadGateway

config = Config()

logger = logging.getLogger(__name__)


class HttpHandler:
    _limit: int = config.getint("gateway", "connections")

    @staticmethod
    async def on_connection_create_start(
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: TraceConnectionCreateStartParams,
    ) -> None:
        logger.debug("Starting connection")

    @staticmethod
    async def on_request_start(
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: TraceRequestStartParams,
    ) -> None:
        logger.debug(f"Starting {params.method} request {params.url}")

    @staticmethod
    async def on_request_end(
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: TraceRequestEndParams,
    ) -> None:
        logger.debug(f"Ending {params.method} request {params.url}")

    @cached_property
    def trace_config(self) -> aiohttp.TraceConfig:
        trace_config = aiohttp.TraceConfig()
        trace_config.on_connection_create_start.append(self.on_connection_create_start)
        trace_config.on_request_start.append(self.on_request_start)
        trace_config.on_request_end.append(self.on_request_end)
        return trace_config

    @property
    def session_options(self) -> dict:
        return dict(
            connector=aiohttp.TCPConnector(limit=self._limit),
            raise_for_status=True,
            trace_configs=[self.trace_config],
        )

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator:
        try:
            async with aiohttp.ClientSession(**self.session_options) as self.session:
                yield

        except aiohttp.ClientError as e:
            raise BadGateway(f"Gateway error: {e}")

        finally:
            delattr(self, "session")
