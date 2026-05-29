# Decision 0002: Builder is plan-only and Pi extension is only a UX handler

Date: 2026-05-29

## Decision

The Kajiya Builder will remain a bounded reasoning step.

The Pi extension should not become the main deterministic execution layer.

## Accepted architecture

    Pi/Pocock extension
      -> prepares prompts and routes operator intent

    Python CLI
      -> status
      -> qa
      -> close-issue
      -> future deterministic evidence commands

    Builder
      -> reads deterministic evidence
      -> produces JSON-compatible patch plans
      -> does not write files
      -> does not commit
      -> does not close issues

## Reason

Kajiya Build Line exists to avoid free-form agent behavior.

The LLM may reason, but deterministic work should be handled by CLI commands that return JSON-compatible outputs and can later be validated with JSON Schema.

## Consequences

- Do not add Gemini SDK to Python for Builder.
- Do not make `.pi/extensions/kajiya-build-line.ts` gather complex evidence directly.
- Keep evidence gathering in deterministic commands such as `kajiya-build-line status` and `kajiya-build-line qa`.
- Use `kajiya-build-line close-issue` for backlog transitions.
- Future Builder improvements should focus on better prompts, schemas, and validation, not autonomous execution.
