# kajiya_onboard_project

## Purpose

Discover the current repository and determine whether it is ready for Kajiya Build Line work.

This is the first pi.dev-style step executed by the Kajiya Build Line handler.

## Safety

- Read-only.
- No file modifications.
- No project-specific memory.
- No external writes.
- Does not assume the repository is kajiya-context-engine.

## Required evidence

The onboarding step should inspect, when present:

1. `.kajiya/project.json`
2. `docs/state/current-project.json`
3. `docs/state/backlog.json`
4. `docs/LLM_HANDOFF_PROTOCOL.md`
5. `git status --short`
6. `git --no-pager log --oneline -12`

## Output shape

Return JSON-compatible output with:

- `ok`
- `pi_dev_id`
- `runtime_status`
- `project_root`
- `evidence_read`
- `missing_evidence`
- `inferred_project_type`
- `active_backlog_candidates`
- `next_safe_actions`

## Runtime statuses

- `project_discovered`
- `missing_project_profile`
- `missing_backlog`
- `missing_handoff`
- `not_git_repo`
- `blocked_dirty_worktree`
- `ready_for_backlog_selection`

## Next safe actions

Possible next actions:

- `initialize_project_profile`
- `create_initial_backlog`
- `create_handoff_protocol`
- `select_backlog_item`
- `run_backlog_audit`
- `stop`

Writes require explicit human approval and must be handled by a separate pi.dev.
