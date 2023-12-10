# Extending Tools

To add a new tool:

1. Define typed input/output models in `models.py`
2. Implement tool logic in `tools.py`
3. Call tool in graph node (`src/graph/nodes.py`)
4. Update tests for schema and smoke behavior

Keep tools deterministic where possible for stable CI and eval reproducibility.
