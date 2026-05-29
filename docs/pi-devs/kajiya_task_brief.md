# kajiya_task_brief

## Purpose

Record a human-authored surgical instruction for the Builder.

Evidence is for the human operator and handler to understand the situation. The Builder should receive a curated task brief, not raw repository evidence.

## Command

    kajiya-build-line task-brief --issue-id KBL-008 --instruction "..." --evidence docs/evidence/example.md --allowed-file src/example.py --validation "kajiya-build-line qa"

## Safety

- Local write only.
- Writes only under `docs/task-briefs/`.
- Does not invoke LLMs.
- Does not modify source code.
- Does not commit.
- Does not close issues.
- Requires human-authored instruction.

## Inputs

Required:

- `--issue-id`
- `--instruction`

Optional repeatable:

- `--evidence`
- `--allowed-file`
- `--validation`
- `--forbidden-action`

## Output

Returns JSON-compatible output with:

- `schema_version`
- `kind`
- `ok`
- `pi_dev_id`
- `runtime_status`
- `issue_id`
- `brief_path`
- `updated_files`
- `next_safe_actions`

## Rule

Raw evidence informs the operator.

Task brief instructs the Builder.
