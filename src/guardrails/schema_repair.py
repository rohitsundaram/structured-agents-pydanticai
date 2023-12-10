from __future__ import annotations

from typing import Any


def repair_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Minimal deterministic repair pass before fallback.
    """
    fixed = dict(payload)
    fixed.setdefault("reasons", ["Insufficient structured detail, using conservative policy."])
    fixed.setdefault("missing_fields", [])
    fixed.setdefault("next_questions", [])
    fixed.setdefault("policy_flags", [])
    fixed.setdefault("confidence", 0.5)
    if fixed.get("risk_impact") not in {"Critical", "High", "Moderate", "Low"}:
        fixed["risk_impact"] = "High"
    return fixed
