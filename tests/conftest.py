from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from muwajjih.adapters.model.sklearn import SklearnDepartmentModel
from muwajjih.api.app import create_app
from muwajjih.domain.models import Department
from muwajjih.service.triage import TriageService
from tests.doubles import ConstantDepartmentModel

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "src" / "muwajjih" / "adapters" / "model" / "artifacts" / "classifier.joblib"


@pytest.fixture
def client_factory():
    def make_client(department: Department = Department.ROADS) -> TestClient:
        model = ConstantDepartmentModel(department)
        service = TriageService(model=model)
        return TestClient(create_app(service_override=service), raise_server_exceptions=False)

    return make_client


@pytest.fixture(scope="session")
def real_model() -> SklearnDepartmentModel:
    model = SklearnDepartmentModel(MODEL_PATH)
    model.load()
    model.warm_up()
    return model
