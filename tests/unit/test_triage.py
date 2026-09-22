import pytest

from muwajjih.domain.models import Complaint, Department, Priority
from muwajjih.service.triage import TriageService

pytestmark = pytest.mark.unit


class FakeModel:
    def __init__(self, department: Department) -> None:
        self.department = department

    def predict_department(self, complaint_text: str) -> Department:
        return self.department


class FakeRepository:
    def __init__(self) -> None:
        self.saved = None

    def save(self, trace_id, result) -> None:
        self.saved = (trace_id, result)


def test_service_uses_model_for_department():
    service = TriageService(FakeModel(Department.ROADS))
    result = service.triage(Complaint("large pothole on the road"), "trace-1")
    assert result.department is Department.ROADS
    assert result.priority is Priority.NORMAL


def test_service_emergency_rule_overrides_priority():
    service = TriageService(FakeModel(Department.BUILDING))
    result = service.triage(Complaint("There is a fire in the building"), "trace-2")
    assert result.priority is Priority.URGENT


def test_service_persists_when_repository_exists():
    repository = FakeRepository()
    service = TriageService(FakeModel(Department.WASTE), repository)
    result = service.triage(Complaint("trash is overflowing"), "trace-3")
    assert repository.saved == ("trace-3", result)