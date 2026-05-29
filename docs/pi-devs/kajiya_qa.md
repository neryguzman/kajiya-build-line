# kajiya_qa

## Purpose

Run deterministic validation checks for the current repository.

## Safety

- Read-only.
- No external writes.
- No file modifications.
- No LLM required.

## Default checks

- `git --no-pager diff --check`
- `python -m compileall src`

## Output

Returns JSON-compatible output with:

- `ok`
- `pi_dev_id`
- `runtime_status`
- `checks`
- `failures`
- `next_safe_actions`

## Runtime statuses

- `qa_passed`
- `qa_failed`
- `qa_partially_available`
