import pytest

from muwajjih.domain.models import Complaint, Department, Priority
from muwajjih.service.triage import TriageService
from tests.doubles import ConstantDepartmentModel

pytestmark = pytest.mark.unit


def test_simulated_model_controls_department_without_sklearn():
    model = ConstantDepartmentModel(Department.LIGHTING)
    service = TriageService(model=model)
    result = service.triage(Complaint("Street light is broken"), "unit-test")
    assert result.department is Department.LIGHTING
    assert result.priority is Priority.NORMAL


def test_emergency_rule_overrides_priority_with_simulated_model():
    model = ConstantDepartmentModel(Department.ROADS)
    service = TriageService(model=model)
    result = service.triage(Complaint("There is a fire in the building"), "unit-test")
    assert result.department is Department.ROADS
    assert result.priority is Priority.URGENT
