# Prompting Guide

For production-style reliability:

- Ask for strict JSON output only
- Ask model to cite evidence from input and tool output
- Keep prompts short and policy-driven
- Separate extraction from classification when possible

This repo uses deterministic rules for classifier behavior and leaves prompt hooks for future LLM integration.
