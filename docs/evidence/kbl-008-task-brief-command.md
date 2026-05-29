# KBL-008 Evidence: human-authored task brief command

Date: 2026-05-29

## Implemented

Added deterministic task brief support through:

    kajiya-build-line task-brief

## Files added/updated

- `src/kajiya_build_line/task_brief.py`
- `src/kajiya_build_line/cli.py`
- `docs/pi-devs/kajiya_task_brief.md`
- `docs/schemas/kajiya-task-brief.schema.json`
- `docs/task-briefs/KBL-008.json`

## Validation

The following command passed:

    kajiya-build-line task-brief --issue-id KBL-008 --instruction "Implement task-brief command. Do not modify Pi extension." --evidence docs/evidence/kbl-007-evidence-command.md --allowed-file src/kajiya_build_line/cli.py --allowed-file src/kajiya_build_line/task_brief.py --validation "kajiya-build-line qa"

The command returned:

- `schema_version`: `kajiya.task_brief_result.v1`
- `kind`: `kajiya_task_brief_result`
- `ok`: true
- `pi_dev_id`: `kajiya_task_brief`
- `runtime_status`: `task_brief_created`
- `brief_path`: `docs/task-briefs/KBL-008.json`

Additional validation passed:

    kajiya-build-line status
    kajiya-build-line qa
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Kajiya Build Line now separates raw evidence from Builder instruction.

Raw evidence informs the operator.

Task brief instructs the Builder.

This prevents raw context stuffing and preserves the human-authored surgical instruction as a durable JSON artifact.
