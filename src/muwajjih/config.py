from __future__ import annotations

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MUWAJJIH_", env_file=".env", extra="ignore")

    environment: str = "development"
    model_path: str = "src/muwajjih/adapters/model/artifacts/classifier.joblib"
    supabase_url: str | None = None
    supabase_key: str | None = None
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    @model_validator(mode="after")
    def validate_supabase_pair(self) -> "Settings":
        if bool(self.supabase_url) != bool(self.supabase_key):
            raise ValueError("Supabase URL and key must be provided together")
        return self
