from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.graph.risk_graph import run_risk_workflow
from src.utils.tracing import write_run_trace


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    risk = sub.add_parser("risk")
    risk.add_argument("--input", required=True, help="JSONL file of change request objects")
    return p.parse_args()


def run_risk(jsonl_path: str) -> None:
    rows = []
    with Path(jsonl_path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    outputs = []
    for idx, row in enumerate(rows, start=1):
        result, trace = run_risk_workflow(row)
        payload = {"input": row, "output": result.model_dump(), "trace": trace}
        outputs.append(payload)
        print(json.dumps(payload, indent=2))
        write_run_trace(f"risk_run_{idx}.json", payload)

    print(f"Processed {len(outputs)} items.")


def main() -> None:
    args = parse_args()
    if args.command == "risk":
        run_risk(args.input)


if __name__ == "__main__":
    main()
