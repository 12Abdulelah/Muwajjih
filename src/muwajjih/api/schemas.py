from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from muwajjih.domain.models import Department, Priority


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    complaint: str = Field(min_length=1, max_length=2000)

    @field_validator("complaint")
    @classmethod
    def complaint_must_contain_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("complaint must not be blank")
        return cleaned


class PredictionData(BaseModel):
    department: Department
    priority: Priority


class ErrorData(BaseModel):
    code: str
    message: str


class ResponseEnvelope(BaseModel):
    trace_id: str
    data: PredictionData | dict[str, Any] | None
    error: ErrorData | None
