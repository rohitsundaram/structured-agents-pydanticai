from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_repair_retries: int = int(os.getenv("MAX_REPAIR_RETRIES", "2"))


settings = Settings()
