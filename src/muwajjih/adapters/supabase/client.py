from __future__ import annotations

from typing import Any


def create_supabase_client(url: str, key: str) -> Any:
    from supabase import create_client

    return create_client(url, key)
