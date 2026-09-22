import json
from pathlib import Path

import pytest


MALFORMED = sorted((Path(__file__).resolve().parents[2] / "payloads" / "malformed").glob("*.json"))
pytestmark = pytest.mark.integration


@pytest.mark.parametrize("payload_file", MALFORMED)
def test_malformed_corpus_is_rejected(client_factory, payload_file):
    with client_factory() as client:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
        response = client.post("/v1/predict", json=payload)
    assert 400 <= response.status_code < 500
    assert response.json()["error"]["code"] == "validation_error"
