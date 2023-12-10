from __future__ import annotations


def search_runbook(query: str) -> list[str]:
    base = "https://runbooks.example.internal"
    return [f"{base}/incident/{query.replace(' ', '-').lower()}", f"{base}/ops/general-triage"]
