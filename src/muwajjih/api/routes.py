from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from muwajjih.api.schemas import PredictionData, PredictRequest, ResponseEnvelope
from muwajjih.domain.models import Complaint
from muwajjih.service.triage import TriageService


def get_triage_service(request: Request) -> TriageService:
    service = getattr(request.app.state, "triage_service", None)

    if service is None:
        raise RuntimeError("Triage service is not ready")

    return service


router = APIRouter()


@router.get("/health", response_model=ResponseEnvelope)
def health(request: Request) -> ResponseEnvelope:
    return ResponseEnvelope(
        trace_id=request.state.trace_id,
        data={"status": "alive"},
        error=None,
    )


@router.get("/ready", response_model=ResponseEnvelope)
def ready(request: Request, response: Response) -> ResponseEnvelope:
    is_ready = bool(getattr(request.app.state, "ready", False))

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    readiness_status = "ready" if is_ready else "not_ready"

    return ResponseEnvelope(
        trace_id=request.state.trace_id,
        data={"status": readiness_status},
        error=None,
    )


@router.post("/v1/predict", response_model=ResponseEnvelope)
def predict(
    payload: PredictRequest,
    request: Request,
    service: Annotated[TriageService, Depends(get_triage_service)],
) -> ResponseEnvelope:
    result = service.triage(
        Complaint(text=payload.complaint),
        request.state.trace_id,
    )

    data = PredictionData(
        department=result.department,
        priority=result.priority,
    )

    return ResponseEnvelope(
        trace_id=request.state.trace_id,
        data=data,
        error=None,
    )