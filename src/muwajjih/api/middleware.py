from __future__ import annotations

import logging
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from muwajjih.logging_config import trace_id_context


logger = logging.getLogger("muwajjih.requests")


class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
        token = trace_id_context.set(trace_id)
        request.state.trace_id = trace_id
        try:
            response = await call_next(request)
            response.headers["X-Trace-ID"] = trace_id
            logger.info("request_completed method=%s path=%s status=%s", request.method, request.url.path, response.status_code)
            return response
        finally:
            trace_id_context.reset(token)
