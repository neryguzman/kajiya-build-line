# kajiya_status

## Purpose

Produce deterministic project status JSON for the current repository.

This is the CLI/deterministic counterpart to the read-only onboarding prompt.

## Safety

- Read-only.
- No external writes.
- No file modifications.
- No LLM required.

## Inputs

Optional:

- `--json`

## Evidence read

- `.kajiya/project.json`
- `docs/state/current-project.json`
- `docs/state/backlog.json`
- `docs/LLM_HANDOFF_PROTOCOL.md`
- `git status --short`
- `git --no-pager log --oneline -12`

## Output

Returns JSON-compatible output with:

- `ok`
- `pi_dev_id`
- `runtime_status`
- `project_root`
- `project_profile`
- `current_project`
- `backlog_summary`
- `git`
- `missing_evidence`
- `next_safe_actions`

## Runtime statuses

- `ready_for_backlog_selection`
- `missing_project_profile`
- `missing_backlog`
- `missing_handoff`
- `not_git_repo`
- `dirty_worktree`
