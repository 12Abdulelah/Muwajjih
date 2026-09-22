from __future__ import annotations

import logging
from typing import Any

from muwajjih.domain.models import TriageResult


logger = logging.getLogger("muwajjih.supabase")


class SupabasePredictionRepository:
    def __init__(self, client: Any) -> None:
        self.client = client

    def save(self, trace_id: str, result: TriageResult) -> None:
        payload = {
            "trace_id": trace_id,
            "department": result.department.value,
            "priority": result.priority.value,
        }
        try:
            self.client.table("triage_predictions").insert(payload).execute()
        except Exception:
            logger.warning("prediction_persistence_failed")
