from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.agents.risk_classifier.models import RiskClassificationOutput


def test_risk_output_schema_success() -> None:
    obj = RiskClassificationOutput(
        risk_impact="High",
        confidence=0.82,
        reasons=["Production deployment detected", "Rollback plan not explicit"],
        missing_fields=[],
        next_questions=[],
        policy_flags=[],
        needs_human_review=True,
    )
    assert obj.risk_impact == "High"


def test_risk_output_reasons_minimum() -> None:
    with pytest.raises(ValidationError):
        RiskClassificationOutput(
            risk_impact="Low",
            confidence=0.4,
            reasons=["single reason only"],
            missing_fields=[],
            next_questions=[],
            policy_flags=[],
            needs_human_review=False,
        )
