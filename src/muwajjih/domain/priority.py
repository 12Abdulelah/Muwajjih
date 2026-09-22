from __future__ import annotations

import re

from muwajjih.domain.models import Priority


_EMERGENCY_PATTERNS = (
    re.compile(r"\bfire\b", re.IGNORECASE),
    re.compile(r"\bflames?\b", re.IGNORECASE),
    re.compile(r"\bburning\b", re.IGNORECASE),
    re.compile(r"\bgas\s+leak(?:ing)?\b", re.IGNORECASE),
    re.compile(r"\bgas\s+is\s+leaking\b", re.IGNORECASE),
    re.compile(r"\bsmell(?:ing)?\s+(?:of\s+)?gas\b", re.IGNORECASE),
    re.compile(r"\bgas\s+smell\b", re.IGNORECASE),
    re.compile(r"حريق"),
    re.compile(r"نار"),
    re.compile(r"تسرب\s+غاز"),
    re.compile(r"تسرّب\s+غاز"),
)


def priority_for(complaint_text: str) -> Priority:
    if any(pattern.search(complaint_text) for pattern in _EMERGENCY_PATTERNS):
        return Priority.URGENT
    return Priority.NORMAL
