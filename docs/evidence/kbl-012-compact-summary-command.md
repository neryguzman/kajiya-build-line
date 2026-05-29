# KBL-012 Evidence: compact status summary command

Date: 2026-05-29

## Implemented

Added compact operator dashboard support through:

    kajiya-build-line summary

## Files added/updated

- `src/kajiya_build_line/summary.py`
- `src/kajiya_build_line/cli.py`

## Validation

The following command passed:

    kajiya-build-line summary

The command returned:

- `schema_version`: `kajiya.summary.v1`
- `kind`: `kajiya_summary`
- `ok`: true
- `pi_dev_id`: `kajiya_summary`
- `runtime_status`: `summary_ready`
- `active_issue_id`: `KBL-012`
- `dirty`: false
- `qa.ok`: true
- `validation.ok`: true
- `validation.runtime_status`: `json_validation_passed`

Additional validation passed:

    kajiya-build-line qa
    kajiya-build-line validate-json
    kajiya-build-line status
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Kajiya Build Line now has a compact operator-facing status command.

The full JSON outputs remain available for deep inspection, but the operator can now use `summary` as the daily cockpit view for quick decision-making.
