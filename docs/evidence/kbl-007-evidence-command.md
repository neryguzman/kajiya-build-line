# KBL-007 Evidence: deterministic evidence collection command

Date: 2026-05-29

## Implemented

Added deterministic evidence collection support through:

    kajiya-build-line evidence

## Files added/updated

- `src/kajiya_build_line/evidence.py`
- `src/kajiya_build_line/cli.py`
- `docs/pi-devs/kajiya_evidence.md`
- `docs/schemas/kajiya-evidence.schema.json`

## Validation

The following command passed:

    kajiya-build-line evidence --read docs/state/backlog.json --list src/kajiya_build_line --grep close_issue --grep-path src --git-log 5

The command returned:

- `schema_version`: `kajiya.evidence.v1`
- `kind`: `kajiya_evidence`
- `ok`: true
- `pi_dev_id`: `kajiya_evidence`
- `runtime_status`: `evidence_collected`

Additional validation passed:

    kajiya-build-line status
    kajiya-build-line qa
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Kajiya Build Line can now gather read-only project evidence deterministically.

This reduces reliance on free-form shell commands invented by an LLM and gives the Builder clean JSON-compatible evidence as input.

## Close criteria check

- Evidence command supports safe file reads: passed.
- Evidence command supports directory listings: passed.
- Evidence command supports grep over an explicit path: passed.
- Evidence command supports git log summary: passed.
- Command returns JSON-compatible output: passed.
- Command is read-only: passed.
- QA passes: passed.
