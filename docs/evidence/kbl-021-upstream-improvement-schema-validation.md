# KBL-021 Evidence: upstream improvement schema validation

Date: 2026-05-29

## Implemented

Added JSON Schema validation for upstream improvement proposal artifacts.

## Files added/updated

- `docs/schemas/kajiya-upstream-improvement.schema.json`
- `src/kajiya_build_line/validate_json.py`

## Behavior

`kajiya-build-line validate-json` now validates upstream improvement artifacts under:

    docs/upstream-improvements/*.json

against:

    docs/schemas/kajiya-upstream-improvement.schema.json

## Validation

The command:

    kajiya-build-line validate-json

validated:

- `.kajiya/project.json`
- `docs/task-briefs/KBL-008.json`
- `docs/upstream-improvements/fix-agents-bootstrap-regression.json`

All returned:

- `ok`: true
- `runtime_status`: `schema_validation_passed`

The QA gate also passed and included:

- `git_diff_check`
- `python_compileall_src`
- `json_schema_validation`

Additional validation passed:

    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Upstream improvement proposals are now contract-validated durable JSON artifacts.

This closes the loop introduced by KBL-020:

    child repo discovers reusable improvement
      -> upstream-improvement proposal artifact
      -> schema validation
      -> QA gate
      -> upstream backlog/task brief/PR flow

Kajiya Build Line now protects its framework-improvement feedback loop with JSON Schema.
