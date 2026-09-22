from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from muwajjih.domain.models import Department


class SklearnDepartmentModel:
    def __init__(self, model_path: str | Path) -> None:
        self.model_path = Path(model_path)
        self.pipeline: Any | None = None
        self.warmed_up = False

    @property
    def loaded(self) -> bool:
        return self.pipeline is not None

    def load(self) -> None:
        self.pipeline = joblib.load(self.model_path)

    def warm_up(self) -> None:
        if self.pipeline is None:
            raise RuntimeError("Model is not loaded")
        self.predict_department("street light is not working")
        self.warmed_up = True

    def predict_department(self, complaint_text: str) -> Department:
        if self.pipeline is None:
            raise RuntimeError("Model is not loaded")
        prediction = self.pipeline.predict([complaint_text])[0]
        return Department(str(prediction))
