from __future__ import annotations

from src.agents.risk_classifier.models import ChangeFields, RiskClassificationOutput


def classify_by_rules(fields: ChangeFields) -> RiskClassificationOutput:
    reasons: list[str] = []
    missing: list[str] = []
    next_questions: list[str] = []
    policy_flags: list[str] = []
    confidence = 0.72

    if not fields.environment:
        missing.append("environment")
        next_questions.append("Which environment is targeted (production/staging)?")
    if fields.has_rollback_plan is None:
        missing.append("rollback_plan")
        next_questions.append("Is there a tested rollback plan?")

    risk = "Moderate"
    if fields.mentions_payment_or_identity:
        risk = "High"
        reasons.append("Mentions payment or identity surface, which is policy-critical.")
    if fields.mentions_database:
        risk = "High"
        reasons.append("Includes database/schema signal, increasing blast radius.")
    if fields.has_rollback_plan is False:
        risk = "Critical"
        reasons.append("Rollback plan appears missing or explicitly absent.")
        policy_flags.append("NO_ROLLBACK")

    if fields.environment == "production":
        reasons.append("Targets production environment.")
    else:
        confidence -= 0.08

    if not reasons:
        reasons = [
            "Change looks constrained but lacks strong risk amplifiers.",
            "No payment/identity/database indicators were detected.",
        ]
        risk = "Low" if not missing else "Moderate"

    return RiskClassificationOutput(
        risk_impact=risk,  # type: ignore[arg-type]
        confidence=max(0.0, min(1.0, confidence)),
        reasons=reasons,
        missing_fields=missing,
        next_questions=next_questions,
        policy_flags=policy_flags,
        needs_human_review=(risk in {"Critical", "High"} or bool(missing)),
    )
