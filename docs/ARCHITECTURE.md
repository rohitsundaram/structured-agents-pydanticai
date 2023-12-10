# Architecture

Risk workflow (LangGraph state machine):

1. `sanitize_input`
   - PII redaction and policy flagging
2. `extract_fields`
   - Typed field extraction tool
3. `classify_risk`
   - Typed classifier output candidate
4. `validate_output`
   - Strict Pydantic validation + grounding check
5. Branching
   - valid -> finalize
   - invalid + retries left -> repair and retry
   - invalid + retries exhausted -> safe fallback

This gives deterministic bounded loops and audit-friendly traces.
