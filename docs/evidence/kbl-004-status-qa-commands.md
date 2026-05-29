# KBL-004 Evidence: Deterministic status and QA commands

Date: 2026-05-29

## Commands tested

    kajiya-build-line status
    kajiya-build-line qa

## Status result

`kajiya-build-line status` returned JSON-compatible output with:

- `schema_version`: `kajiya.status.v1`
- `kind`: `kajiya_status`
- `ok`: true
- `pi_dev_id`: `kajiya_status`
- `runtime_status`: `ready_for_backlog_selection`
- `missing_evidence`: []
- clean git status
- active backlog candidates including `KBL-004` and `KBL-005`

## QA result

`kajiya-build-line qa` returned JSON-compatible output with:

- `schema_version`: `kajiya.qa.v1`
- `kind`: `kajiya_qa`
- `ok`: true
- `pi_dev_id`: `kajiya_qa`
- `runtime_status`: `qa_passed`

Checks passed:

- `git --no-pager diff --check`
- `python -m compileall src`

## Architectural significance

This completes the transition from prompt-only onboarding toward deterministic CLI execution.

The Build Line can now inspect project state and run QA without relying on LLM reasoning.

## Close criteria check

- Status works from this repo: passed.
- QA is read-only and deterministic: passed.
- Output is JSON-compatible: passed.
- Python sources compile: passed.
- Git diff check passes: passed.
