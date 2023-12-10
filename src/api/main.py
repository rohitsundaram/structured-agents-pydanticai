from __future__ import annotations

from fastapi import FastAPI

from src.agents.incident_triage.models import IncidentInput, IncidentOutput
from src.agents.risk_classifier.models import ChangeRequestInput, RiskClassificationOutput
from src.graph.incident_graph import run_incident_workflow
from src.graph.risk_graph import run_risk_workflow

app = FastAPI(title="Structured Agents PydanticAI")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/risk/classify", response_model=RiskClassificationOutput)
def classify_risk(req: ChangeRequestInput) -> RiskClassificationOutput:
    output, _trace = run_risk_workflow(req.model_dump())
    return output


@app.post("/incident/triage", response_model=IncidentOutput)
def triage_incident(req: IncidentInput) -> IncidentOutput:
    return run_incident_workflow(req.model_dump())
