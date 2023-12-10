from __future__ import annotations

from src.agents.risk_classifier.models import ChangeRequestInput, RiskClassificationOutput
from src.agents.risk_classifier.rules import classify_by_rules
from src.agents.risk_classifier.tools import (
    check_maintenance_window,
    extract_change_fields,
    lookup_service_criticality,
)


def run_risk_classifier(req: ChangeRequestInput) -> RiskClassificationOutput:
    fields = extract_change_fields(req.change_text)
    if req.service_name and not fields.service_name:
        fields.service_name = req.service_name
    if req.environment and not fields.environment:
        fields.environment = req.environment
    if req.has_rollback_plan is not None:
        fields.has_rollback_plan = req.has_rollback_plan

    result = classify_by_rules(fields)

    criticality = lookup_service_criticality(fields.service_name)
    in_window = check_maintenance_window(req.scheduled_window_utc)
    if criticality == "critical" and result.risk_impact in {"Moderate", "Low"}:
        result.risk_impact = "High"
        result.reasons.append("Service criticality lookup escalated risk to High.")
        result.policy_flags.append("CRITICAL_SERVICE")
    if in_window is False:
        result.policy_flags.append("OUTSIDE_MAINTENANCE_WINDOW")
        if result.risk_impact != "Critical":
            result.risk_impact = "High"
            result.reasons.append("Scheduled window is outside recommended maintenance hours.")

    return result
