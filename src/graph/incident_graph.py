from __future__ import annotations

from src.agents.incident_triage.agent import run_incident_triage
from src.agents.incident_triage.models import IncidentInput, IncidentOutput


def run_incident_workflow(payload: dict) -> IncidentOutput:
    req = IncidentInput(**payload)
    return run_incident_triage(req)
