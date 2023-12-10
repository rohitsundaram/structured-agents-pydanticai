from __future__ import annotations

from src.agents.incident_triage.models import IncidentInput, IncidentOutput


def run_incident_triage(req: IncidentInput) -> IncidentOutput:
    text = req.incident_text.lower()
    if "timeout" in text or "latency" in text:
        return IncidentOutput(
            category="performance",
            severity="high",
            routing_team="platform-sre",
            runbook_links=["https://runbooks.example.internal/perf"],
            immediate_actions=["Scale read replicas", "Check dependency health"],
        )
    return IncidentOutput(
        category="application",
        severity="moderate",
        routing_team="service-team",
        runbook_links=["https://runbooks.example.internal/app"],
        immediate_actions=["Review latest deployment diff"],
    )
