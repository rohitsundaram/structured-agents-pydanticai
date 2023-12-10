from __future__ import annotations

from pydantic import ValidationError

from src.agents.risk_classifier.agent import run_risk_classifier
from src.agents.risk_classifier.models import ChangeRequestInput, RiskClassificationOutput
from src.agents.risk_classifier.tools import extract_change_fields
from src.graph.state import RiskGraphState
from src.guardrails.pii import redact_pii
from src.guardrails.safety import enforce_reason_grounding
from src.guardrails.schema_repair import repair_payload


def sanitize_input(state: RiskGraphState) -> RiskGraphState:
    change_text = str(state.original_input.get("change_text", ""))
    redacted, flags = redact_pii(change_text)
    state.sanitized_text = redacted
    state.policy_flags.extend(flags)
    return state


def extract_fields(state: RiskGraphState) -> RiskGraphState:
    state.fields = extract_change_fields(state.sanitized_text)
    return state


def classify_risk(state: RiskGraphState) -> RiskGraphState:
    req = ChangeRequestInput(**{**state.original_input, "change_text": state.sanitized_text})
    output = run_risk_classifier(req)
    payload = output.model_dump()
    payload["policy_flags"] = list(dict.fromkeys(payload["policy_flags"] + state.policy_flags))
    state.candidate_output = payload
    return state


def validate_output(state: RiskGraphState) -> RiskGraphState:
    if state.candidate_output is None:
        state.errors.append("MISSING_CANDIDATE_OUTPUT")
        return state
    try:
        validated = RiskClassificationOutput(**state.candidate_output)
        extra_flags = enforce_reason_grounding(validated, state.sanitized_text)
        validated.policy_flags = list(dict.fromkeys(validated.policy_flags + extra_flags))
        state.final_output = validated
    except ValidationError as exc:
        state.errors.append(f"VALIDATION_ERROR: {exc.errors()[0].get('msg', 'unknown')}")
    return state


def repair_output(state: RiskGraphState) -> RiskGraphState:
    if state.candidate_output is None:
        state.candidate_output = {}
    state.candidate_output = repair_payload(state.candidate_output)
    state.repair_attempts += 1
    return state
