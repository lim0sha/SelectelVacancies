from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )
    database_url: str = Field(..., validation_alias="DATABASE_URL")
    app_port: int
    log_level: str
    debug: bool = False
    cors_origins: List[str] = ["*"]
    parse_schedule_minutes: int
    external_vacancies_api_url: str


settings = Settings()
