# kajiya_evidence

## Purpose

Collect read-only project evidence deterministically.

This command lets the operator gather file contents, directory listings, grep matches, and git log output without asking an LLM to invent shell commands.

## Command

    kajiya-build-line evidence --read docs/state/backlog.json --list src/kajiya_build_line --grep close_issue --grep-path src --git-log 5

## Safety

- Read-only.
- No external writes.
- No file modifications.
- Paths are constrained to the project root.
- Output is JSON-compatible.

## Inputs

Optional and repeatable:

- `--read PATH`
- `--list PATH`
- `--grep TEXT`
- `--grep-path PATH`
- `--git-log N`

## Output

Returns:

- `schema_version`
- `kind`
- `ok`
- `pi_dev_id`
- `runtime_status`
- `project_root`
- `request`
- `results`
- `next_safe_actions`

## Runtime statuses

- `evidence_collected`
- `evidence_partial_or_failed`
