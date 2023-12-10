from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChangeRequestInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    change_text: str = Field(min_length=10)
    service_name: str | None = None
    environment: str | None = None
    has_rollback_plan: bool | None = None
    scheduled_window_utc: str | None = None


class ChangeFields(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service_name: str | None = None
    environment: str | None = None
    has_rollback_plan: bool | None = None
    mentions_database: bool = False
    mentions_payment_or_identity: bool = False


class RiskClassificationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    risk_impact: Literal["Critical", "High", "Moderate", "Low"]
    confidence: float = Field(ge=0, le=1)
    reasons: list[str] = Field(min_length=2)
    missing_fields: list[str] = Field(default_factory=list)
    next_questions: list[str] = Field(default_factory=list)
    policy_flags: list[str] = Field(default_factory=list)
    needs_human_review: bool = False

    @field_validator("reasons")
    @classmethod
    def validate_reason_length(cls, v: list[str]) -> list[str]:
        cleaned = [x.strip() for x in v if x.strip()]
        if len(cleaned) < 2:
            raise ValueError("At least two non-empty reasons required")
        return cleaned
