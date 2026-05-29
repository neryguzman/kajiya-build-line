# KBL-011 Evidence: JSON Schema validation in QA gate

Date: 2026-05-29

## Implemented

Added JSON Schema validation as a standard `kajiya-build-line qa` check.

## Files updated

- `src/kajiya_build_line/qa.py`

## Validation

The following command passed:

    kajiya-build-line qa

QA now includes:

- `git_diff_check`
- `python_compileall_src`
- `json_schema_validation`

The new check returned:

- `name`: `json_schema_validation`
- `ok`: true
- `runtime_status`: `json_validation_passed`

The following command also passed independently:

    kajiya-build-line validate-json

## Architectural significance

QA now acts as a real deterministic gate for both code and durable JSON artifacts.

Kajiya Build Line now validates:

- Git diff whitespace/check issues
- Python compilation
- JSON Schema contracts

This makes the Build Line safer before commits, issue closures, and future Builder-assisted work.
