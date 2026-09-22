import pytest

from muwajjih.domain.models import Department

pytestmark = pytest.mark.integration


def test_predict_contract_with_simulated_model(client_factory):
    with client_factory(Department.LIGHTING) as client:
        response = client.post("/v1/predict", json={"complaint": "A street light is broken"})
    body = response.json()
    assert response.status_code == 200
    assert body["data"]["department"] == "lighting"
    assert body["data"]["priority"] == "normal"
    assert body["error"] is None
    assert body["trace_id"]
    assert response.headers["X-Trace-ID"] == body["trace_id"]


def test_simulated_model_cannot_override_emergency_policy(client_factory):
    with client_factory(Department.PARKS) as client:
        response = client.post("/v1/predict", json={"complaint": "There is a gas leak"})
    assert response.status_code == 200
    assert response.json()["data"]["department"] == "parks"
    assert response.json()["data"]["priority"] == "urgent"


def test_ready_is_true_with_simulated_service(client_factory):
    with client_factory() as client:
        response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ready"
