from __future__ import annotations

import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{2,4}[-.\s]?){2,4}\d{2,4}\b")


def redact_pii(text: str) -> tuple[str, list[str]]:
    flags: list[str] = []
    redacted = text
    if EMAIL_RE.search(redacted):
        redacted = EMAIL_RE.sub("[REDACTED_EMAIL]", redacted)
        flags.append("PII_DETECTED_EMAIL")
    if PHONE_RE.search(redacted):
        redacted = PHONE_RE.sub("[REDACTED_PHONE]", redacted)
        flags.append("PII_DETECTED_PHONE")
    return redacted, flags
