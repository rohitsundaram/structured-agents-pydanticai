from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.agents.risk_classifier.models import RiskClassificationOutput
from src.graph.nodes import classify_risk, extract_fields, repair_output, sanitize_input, validate_output
from src.graph.policies import safe_fallback
from src.graph.state import RiskGraphState
from src.utils.config import settings


def _route_after_validation(state: RiskGraphState) -> str:
    if state.final_output is not None:
        return "finalize"
    if state.repair_attempts < state.max_retries:
        return "repair"
    return "fallback"


def run_risk_workflow(payload: dict) -> tuple[RiskClassificationOutput, dict]:
    initial_state = RiskGraphState(
        original_input=payload,
        max_retries=settings.max_repair_retries,
    )

    graph = StateGraph(RiskGraphState)
    graph.add_node("sanitize", sanitize_input)
    graph.add_node("extract", extract_fields)
    graph.add_node("classify", classify_risk)
    graph.add_node("validate", validate_output)
    graph.add_node("repair", repair_output)
    graph.add_node("finalize", lambda s: s)
    graph.add_node("fallback", lambda s: s)

    graph.set_entry_point("sanitize")
    graph.add_edge("sanitize", "extract")
    graph.add_edge("extract", "classify")
    graph.add_edge("classify", "validate")
    graph.add_conditional_edges(
        "validate",
        _route_after_validation,
        {
            "repair": "repair",
            "fallback": "fallback",
            "finalize": "finalize",
        },
    )
    graph.add_edge("repair", "validate")
    graph.add_edge("fallback", END)
    graph.add_edge("finalize", END)

    app = graph.compile()
    out_state = app.invoke(initial_state)
    state = out_state if isinstance(out_state, RiskGraphState) else RiskGraphState(**out_state)

    final = state.final_output or safe_fallback(state.errors)
    trace = {
        "repair_attempts": state.repair_attempts,
        "errors": state.errors,
        "policy_flags": state.policy_flags,
    }
    return final, trace
