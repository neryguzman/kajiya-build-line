# KBL-009 Evidence: JSON Schema validation command

Date: 2026-05-29

## Implemented

Added deterministic JSON Schema validation support through:

    kajiya-build-line validate-json

## Files added/updated

- `pyproject.toml`
- `src/kajiya_build_line/validate_json.py`
- `src/kajiya_build_line/cli.py`
- `docs/pi-devs/kajiya_validate_json.md`
- `docs/schemas/kajiya-validation.schema.json`

## Validation

The following command passed:

    kajiya-build-line validate-json

The command returned:

- `schema_version`: `kajiya.validation.v1`
- `kind`: `kajiya_validation`
- `ok`: true
- `pi_dev_id`: `kajiya_validate_json`
- `runtime_status`: `json_validation_passed`

Validated pairs:

- `.kajiya/project.json` against `docs/schemas/kajiya-project.schema.json`
- `docs/task-briefs/KBL-008.json` against `docs/schemas/kajiya-task-brief.schema.json`

Additional validation passed:

    kajiya-build-line status
    kajiya-build-line qa
    git --no-pager diff --check
    python -m compileall src

## Bug fixed

Initial implementation updated usage text but missed command dispatch for `validate-json`.

Fixed in commit:

    fb11c08 Fix validate-json CLI dispatch

## Architectural significance

Kajiya Build Line now validates durable JSON artifacts against JSON Schema.

This moves the system from convention-based JSON to contract-validated JSON.
