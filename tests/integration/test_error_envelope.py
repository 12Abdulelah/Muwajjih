import pytest
from fastapi.testclient import TestClient

from muwajjih.api.app import create_app
from muwajjih.service.triage_service import TriageService
from tests.doubles import FailingDepartmentModel


pytestmark = pytest.mark.integration


def test_internal_error_uses_safe_envelope():
    app = create_app(service_override=TriageService(FailingDepartmentModel()))
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post("/v1/predict", json={"complaint": "broken light"})
    body = response.json()
    assert response.status_code == 500
    assert body["data"] is None
    assert body["error"]["code"] == "internal_error"
    assert body["error"]["message"] == "Internal server error"
    assert "private stack detail" not in response.text
