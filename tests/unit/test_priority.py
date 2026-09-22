import pytest

from muwajjih.domain.models import Priority
from muwajjih.domain.priority import priority_for

pytestmark = pytest.mark.unit


def test_fire_is_urgent():
    assert priority_for("There is a fire in the building") is Priority.URGENT


def test_gas_leak_is_urgent():
    assert priority_for("There is a gas leak") is Priority.URGENT


def test_gas_leaking_variation_is_urgent():
    assert priority_for("Gas is leaking near the meter") is Priority.URGENT


def test_normal_issue_is_normal():
    assert priority_for("The street light is broken") is Priority.NORMAL