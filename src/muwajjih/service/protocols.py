from __future__ import annotations

from typing import Protocol

from muwajjih.domain.models import Department, TriageResult


class DepartmentModel(Protocol):
    def predict_department(self, complaint_text: str) -> Department:
        ...


class PredictionRepository(Protocol):
    def save(self, trace_id: str, result: TriageResult) -> None:
        ...
