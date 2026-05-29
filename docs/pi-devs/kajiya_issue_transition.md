# kajiya_issue_transition

## Purpose

Close one backlog issue and optionally activate the next issue using a deterministic CLI command.

This replaces ad-hoc pasted Python snippets for backlog/current-project transitions.

## Command

    kajiya-build-line close-issue --issue-id KBL-004 --next-issue-id KBL-005 --evidence docs/evidence/example.md --completion-note "Completed KBL-004."

## Safety

- Local write only.
- No external writes.
- Explicit operator invocation required.
- Does not modify source code.
- Updates only:
  - `docs/state/backlog.json`
  - `docs/state/current-project.json`

## Inputs

Required:

- `--issue-id`
- `--completion-note`

Optional:

- `--next-issue-id`
- `--evidence` one or more paths
- `--commit` commit hash or `pending_commit`

## Output

Returns JSON-compatible output with:

- `schema_version`
- `kind`
- `ok`
- `pi_dev_id`
- `runtime_status`
- `closed_issue_id`
- `activated_issue_id`
- `evidence`
- `updated_files`
- `next_safe_actions`

## Runtime statuses

- `issue_closed`
- `missing_backlog`
- `missing_current_project`
- `issue_not_found`
- `next_issue_not_found`

## Datomic-style note

This transition is currently stored as updates to JSON snapshots.

Future versions may also append immutable transition events so they can be transformed into entity-attribute-value facts.
