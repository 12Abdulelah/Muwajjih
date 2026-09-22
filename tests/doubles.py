from __future__ import annotations

from muwajjih.domain.models import Department


class ConstantDepartmentModel:
    def __init__(self, department: Department = Department.ROADS) -> None:
        self.department = department

    def predict_department(self, complaint_text: str) -> Department:
        return self.department


class FailingDepartmentModel:
    def predict_department(self, complaint_text: str) -> Department:
        raise RuntimeError("private stack detail")
