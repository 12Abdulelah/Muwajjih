from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Priority(StrEnum):
    NORMAL = "normal"
    URGENT = "urgent"


class Department(StrEnum):
    ROADS = "roads"
    LIGHTING = "lighting"
    WASTE = "waste"
    WATER = "water"
    SEWAGE = "sewage"
    PARKS = "parks"
    BUILDING = "building"
    PUBLIC_SAFETY = "public_safety"


@dataclass(frozen=True)
class Complaint:
    text: str


@dataclass(frozen=True)
class TriageResult:
    department: Department
    priority: Priority
