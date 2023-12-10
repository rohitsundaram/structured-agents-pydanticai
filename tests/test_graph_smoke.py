from __future__ import annotations

from src.graph.risk_graph import run_risk_workflow


def test_graph_smoke_runs() -> None:
    output, trace = run_risk_workflow(
        {"change_text": "Deploy payment service update in production without rollback."}
    )
    assert output.risk_impact in {"Critical", "High", "Moderate", "Low"}
    assert isinstance(trace["repair_attempts"], int)
