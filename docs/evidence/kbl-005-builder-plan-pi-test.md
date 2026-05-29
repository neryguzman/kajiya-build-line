# KBL-005 Evidence: bounded builder patch plan Pi test

Date: 2026-05-29

## Test

Ran Pi from the repository root and executed:

    /kajiya-builder-plan issue_id=KBL-005

The command prefilled the Builder prompt in the Pi editor. After pressing Enter, Pi gathered read-only evidence and returned a JSON-compatible patch plan.

## Evidence read by Builder

The Builder inspected:

- `kajiya-build-line status`
- `kajiya-build-line qa`
- `docs/state/backlog.json`
- `docs/state/current-project.json`
- `docs/pi-devs/kajiya_builder_patch_plan.md`
- `docs/schemas/kajiya-builder-patch-plan.schema.json`

## Observed result

The Builder returned:

- `schema_version`: `kajiya.builder_patch_plan.v1`
- `kind`: `kajiya_builder_patch_plan`
- `ok`: true
- `pi_dev_id`: `kajiya_builder_patch_plan`
- `runtime_status`: `builder_plan_ready`
- `issue_id`: `KBL-005`
- `requires_human_approval`: true

## Architectural interpretation

The Builder successfully behaved as a bounded reasoning step.

However, the generated plan suggested adding too much core logic into `.pi/extensions/kajiya-build-line.ts`. The accepted architecture is:

- Pi extension remains UX / prompt launcher.
- Deterministic evidence gathering stays in the Python CLI.
- Builder reasons over evidence.
- Builder does not invoke models directly.
- Builder does not modify files.
- Builder does not close issues.
- Issue transitions use `kajiya-build-line close-issue`.

## Close criteria check

- Builder does not run before backlog issue selection: passed.
- Builder does not use Gemini SDK directly: passed.
- Builder output has next_safe_actions: passed.
- Builder cannot claim files changed unless a deterministic step changed them: passed.
