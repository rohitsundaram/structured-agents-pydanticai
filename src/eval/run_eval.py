from __future__ import annotations

import json
from pathlib import Path

from src.eval.metrics import EvalSummary
from src.graph.risk_graph import run_risk_workflow


def main() -> None:
    path = Path("src/eval/gold_cases.jsonl")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    total = len(rows)
    correct = 0
    invalid = 0
    retries = 0

    for row in rows:
        expected = row["expected_risk_impact"]
        output, trace = run_risk_workflow(row["input"])
        if output.risk_impact == expected:
            correct += 1
        if "SCHEMA_REPAIR_EXHAUSTED" in output.policy_flags:
            invalid += 1
        if trace.get("repair_attempts", 0) > 0:
            retries += 1

    summary = EvalSummary(total=total, correct=correct, invalid_outputs=invalid, retries=retries)
    print(
        json.dumps(
            {
                "total": summary.total,
                "accuracy": round(summary.accuracy, 4),
                "invalid_output_rate": round(summary.invalid_rate, 4),
                "retry_rate": round(summary.retry_rate, 4),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
