from __future__ import annotations

from src.guardrails.pii import redact_pii


def test_pii_redaction_email_phone() -> None:
    text = "Contact me at user@example.com or +971 50 123 4567 for release updates."
    redacted, flags = redact_pii(text)
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_PHONE]" in redacted
    assert "PII_DETECTED_EMAIL" in flags
