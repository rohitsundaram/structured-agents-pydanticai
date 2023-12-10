# Failure Modes

- Missing required fields
  - Example: environment or rollback not present
  - Behavior: populate `missing_fields` + `next_questions`

- Conflicting signals
  - Example: "low risk" text but production DB migration
  - Behavior: risk escalates based on policy rules

- Malformed classifier payload
  - Behavior: schema repair loop attempts deterministic fixes

- Repeated validation failure
  - Behavior: safe fallback output and `needs_human_review=true`
