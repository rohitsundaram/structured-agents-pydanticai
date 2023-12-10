from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)


def write_run_trace(filename: str, payload: dict[str, Any]) -> Path:
    path = RUNS_DIR / filename
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
