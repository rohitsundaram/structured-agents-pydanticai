from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.agents.risk_classifier.models import ChangeFields, RiskClassificationOutput


class RiskGraphState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    original_input: dict[str, Any]
    sanitized_text: str = ""
    fields: ChangeFields | None = None
    candidate_output: dict[str, Any] | None = None
    final_output: RiskClassificationOutput | None = None
    repair_attempts: int = 0
    max_retries: int = 2
    errors: list[str] = Field(default_factory=list)
    policy_flags: list[str] = Field(default_factory=list)
