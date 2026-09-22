import json
from pathlib import Path

import pytest

from muwajjih.domain.models import Complaint, Department, Priority
from muwajjih.service.triage_service import TriageService


GOLDEN_PATH = Path(__file__).with_name("golden.json")
pytestmark = [pytest.mark.behavioural, pytest.mark.slow]


def test_real_model_is_invariant_to_case_for_department(real_model):
    lower = real_model.predict_department("the street light is not working")
    upper = real_model.predict_department("THE STREET LIGHT IS NOT WORKING")
    assert lower is Department.LIGHTING
    assert upper is Department.LIGHTING


def test_real_model_is_invariant_to_extra_whitespace(real_model):
    normal = real_model.predict_department("garbage has not been collected")
    spaced = real_model.predict_department("  garbage   has   not   been   collected  ")
    assert normal is Department.WASTE
    assert spaced is Department.WASTE


def test_directional_emergency_signal_raises_priority(real_model):
    service = TriageService(real_model)
    normal = service.triage(Complaint("The building wall needs inspection"), "normal")
    urgent = service.triage(Complaint("The building wall is on fire"), "urgent")
    assert normal.priority is Priority.NORMAL
    assert urgent.priority is Priority.URGENT


def test_golden_reference_predictions(real_model):
    service = TriageService(real_model)
    cases = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    for case in cases:
        result = service.triage(Complaint(case["complaint"]), "golden")
        assert result.department.value == case["department"]
        assert result.priority.value == case["priority"]


def test_mandatory_fire_and_gas_examples_are_always_urgent(real_model):
    service = TriageService(real_model)
    fire = service.triage(Complaint("There is a fire in the building"), "fire")
    gas = service.triage(Complaint("There is a gas leak"), "gas")
    assert fire.priority is Priority.URGENT
    assert gas.priority is Priority.URGENT


def test_arabic_emergency_extension_is_urgent(real_model):
    service = TriageService(real_model)
    fire = service.triage(Complaint("يوجد حريق في المبنى"), "arabic-fire")
    gas = service.triage(Complaint("يوجد تسرب غاز قرب المبنى"), "arabic-gas")
    assert fire.priority is Priority.URGENT
    assert gas.priority is Priority.URGENT
