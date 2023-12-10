from __future__ import annotations

from src.agents.risk_classifier.models import RiskClassificationOutput


def safe_fallback(errors: list[str]) -> RiskClassificationOutput:
    return RiskClassificationOutput(
        risk_impact="High",
        confidence=0.35,
        reasons=[
            "Output validation failed after bounded retries.",
            "Conservative risk fallback applied by policy.",
        ],
        missing_fields=["manual_review_context"],
        next_questions=["Please review the change request manually and confirm scope and rollback."],
        policy_flags=["SCHEMA_REPAIR_EXHAUSTED"] + errors[-2:],
        needs_human_review=True,
    )
