# KBL-013 Evidence: operator next command

Date: 2026-05-29

## Implemented

Added compact operator guidance through:

    kajiya-build-line next

## Files added/updated

- `src/kajiya_build_line/next_action.py`
- `src/kajiya_build_line/cli.py`

## Validation

The following command passed:

    kajiya-build-line next

The command returned:

- `schema_version`: `kajiya.next.v1`
- `kind`: `kajiya_next`
- `ok`: true
- `pi_dev_id`: `kajiya_next`
- `runtime_status`: `next_ready`
- `active_issue_id`: `KBL-013`
- `dirty`: false
- `qa_ok`: true
- `validation_ok`: true
- `recommended_action`: Work on KBL-013: implement kajiya-build-line next for compact operator guidance.

Additional validation passed:

    kajiya-build-line summary
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Kajiya Build Line now has a direct operator guidance command.

`summary` answers: what is the project state?

`next` answers: what should the operator do next?

This supports the intended cockpit workflow without forcing the operator to read full JSON outputs every time.
