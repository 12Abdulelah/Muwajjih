from __future__ import annotations

from fastapi import Request

from muwajjih.service.triage import TriageService


def get_triage_service(request: Request) -> TriageService:
    service = getattr(request.app.state, "triage_service", None)

    if service is None:
        raise RuntimeError("Triage service is not ready")

    return service