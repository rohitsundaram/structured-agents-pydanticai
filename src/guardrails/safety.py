from __future__ import annotations

from src.agents.risk_classifier.models import RiskClassificationOutput


def enforce_reason_grounding(output: RiskClassificationOutput, source_text: str) -> list[str]:
    """
    Lightweight anti-hallucination rule:
    if none of the reasons share tokens with source text, mark ambiguous.
    """
    source_tokens = {tok.lower() for tok in source_text.split() if len(tok) > 3}
    reason_tokens = {tok.lower() for r in output.reasons for tok in r.split() if len(tok) > 3}
    if source_tokens and reason_tokens and source_tokens.isdisjoint(reason_tokens):
        return ["UNGROUNDED_REASONING"]
    return []
