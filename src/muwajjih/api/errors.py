from __future__ import annotations

import uuid

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def request_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", str(uuid.uuid4()))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "trace_id": request_trace_id(request),
            "data": None,
            "error": {"code": "validation_error", "message": "Request validation failed"},
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "trace_id": request_trace_id(request),
            "data": None,
            "error": {"code": "internal_error", "message": "Internal server error"},
        },
    )
