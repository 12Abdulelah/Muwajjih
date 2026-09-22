import pytest
from fastapi.testclient import TestClient

from muwajjih.api.app import app

pytestmark = [pytest.mark.integration, pytest.mark.slow]


def test_health_ready_and_real_model_prediction():
    with TestClient(app) as client:
        health = client.get("/health")
        ready = client.get("/ready")
        prediction = client.post(
            "/v1/predict",
            json={"complaint": "The garbage container is full near the market"},
        )
    assert health.status_code == 200
    assert health.json()["data"]["status"] == "alive"
    assert ready.status_code == 200
    assert ready.json()["data"]["status"] == "ready"
    assert prediction.status_code == 200
    assert prediction.json()["data"]["department"] == "waste"
    assert prediction.json()["data"]["priority"] == "normal"


def test_ready_returns_503_when_runtime_is_not_ready():
    with TestClient(app) as client:
        client.app.state.ready = False
        response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["data"]["status"] == "not_ready"
