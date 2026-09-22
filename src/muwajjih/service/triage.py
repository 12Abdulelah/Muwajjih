from __future__ import annotations

from muwajjih.domain.models import Complaint, TriageResult
from muwajjih.domain.priority import priority_for
from muwajjih.service.ports import DepartmentModel, PredictionRepository


class TriageService:
    def __init__(
        self,
        model: DepartmentModel,
        repository: PredictionRepository | None = None,
    ) -> None:
        self.department_model = model
        self.prediction_repository = repository

    def triage(self, complaint: Complaint, trace_id: str) -> TriageResult:
        department = self.department_model.predict_department(complaint.text)
        priority = priority_for(complaint.text)
        result = TriageResult(department=department, priority=priority)
        if self.prediction_repository is not None:
            self.prediction_repository.save(trace_id, result)
        return result
