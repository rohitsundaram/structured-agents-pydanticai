from __future__ import annotations

from datetime import datetime, timezone

from src.agents.risk_classifier.models import ChangeFields


CRITICAL_SERVICES = {"payments", "identity", "auth", "core-banking"}


def extract_change_fields(change_text: str) -> ChangeFields:
    text = change_text.lower()
    service = None
    for name in ["payments", "identity", "auth", "checkout", "notification"]:
        if name in text:
            service = name
            break
    env = "production" if "prod" in text or "production" in text else None
    has_rollback = None
    if "rollback" in text:
        has_rollback = "no rollback" not in text and "without rollback" not in text

    return ChangeFields(
        service_name=service,
        environment=env,
        has_rollback_plan=has_rollback,
        mentions_database=("db" in text or "database" in text or "schema" in text),
        mentions_payment_or_identity=any(x in text for x in ["payment", "identity", "auth"]),
    )


def lookup_service_criticality(service_name: str | None) -> str:
    if not service_name:
        return "unknown"
    return "critical" if service_name.lower() in CRITICAL_SERVICES else "standard"


def check_maintenance_window(scheduled_window_utc: str | None) -> bool | None:
    if not scheduled_window_utc:
        return None
    try:
        dt = datetime.fromisoformat(scheduled_window_utc.replace("Z", "+00:00"))
        hour = dt.astimezone(timezone.utc).hour
        return 0 <= hour <= 5
    except ValueError:
        return None


def search_runbook(query: str) -> list[dict[str, str]]:
    base = "https://runbooks.example.internal"
    return [
        {"title": f"Rollback guide: {query}", "url": f"{base}/rollback"},
        {"title": f"Incident handoff: {query}", "url": f"{base}/handoff"},
    ]
