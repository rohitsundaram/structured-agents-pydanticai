# structured-agents-pydanticai

Typed, guarded, and orchestrated agent workflows for enterprise-style operations use-cases.

## What This Repo Demonstrates

- Typed inputs/outputs and typed tools with Pydantic v2
- Validation failure handling with bounded repair retries
- Guardrails for PII redaction and policy flags
- LangGraph-style state orchestration with branching and loop caps
- API-ready workflow for change request risk classification

## Primary Demo

### Change Request Risk Classifier Agent

Input:
- change request text
- optional fields (service, environment, rollout plan, rollback plan, etc.)

Output:
- `risk_impact`: `Critical | High | Moderate | Low`
- `confidence`: `0..1`
- `reasons[]`
- `missing_fields[]`
- `next_questions[]`
- `policy_flags[]`
- `needs_human_review`

## Architecture (Risk Graph)

`sanitize_input -> extract_fields -> classify_risk -> validate_output`

Branching:
- missing required fields -> ask follow-up questions
- schema validation failure -> repair output (max retry bound)
- repeated failure -> safe fallback + human review flag

See `docs/ARCHITECTURE.md`.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Run CLI on sample change requests:

```bash
python -m src.cli risk --input examples/change_requests.jsonl
```

Run API:

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Test endpoint:

```bash
curl -X POST "http://localhost:8000/risk/classify" \
  -H "Content-Type: application/json" \
  -d '{"change_text":"Deploy payment service patch to production tonight. Rollback not documented."}'
```

## Docker

```bash
docker build -f docker/Dockerfile -t structured-agents-pydanticai .
docker run --rm -p 8000:8000 structured-agents-pydanticai
```

## Evaluation

```bash
python -m src.eval.run_eval
```

Outputs:
- accuracy
- invalid-output rate
- retry rate

## Notes for Enterprise Teams

- Designed for ServiceNow-style change requests
- Policy-first and auditable structured output
- Tool-grounded decisions with deterministic fallback behavior
