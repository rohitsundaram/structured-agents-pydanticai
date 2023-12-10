from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class IncidentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    incident_text: str = Field(min_length=10)
    log_snippet: str | None = None


class IncidentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str
    severity: str
    routing_team: str
    runbook_links: list[str] = Field(default_factory=list)
    immediate_actions: list[str] = Field(default_factory=list)
