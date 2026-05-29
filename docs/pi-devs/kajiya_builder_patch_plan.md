# kajiya_builder_patch_plan

## Purpose

Use Pi/Pocock's configured LLM runtime to produce a bounded implementation plan for a selected backlog issue.

The Builder is a reasoning step, not an executor.

## Safety

- Plan-only.
- No file modifications.
- No external writes.
- No direct Gemini SDK.
- Uses Pi/Pocock configured provider/model.
- Requires a selected `issue_id`.
- Must read deterministic status/QA evidence before planning.

## Required inputs

- `issue_id`

## Required evidence

Before producing a plan, Builder should inspect:

- `kajiya-build-line status`
- `kajiya-build-line qa`
- `docs/state/backlog.json`
- `docs/state/current-project.json`
- relevant pi.dev docs
- relevant schemas

## Output shape

Return JSON-compatible output with:

- `schema_version`
- `kind`
- `ok`
- `pi_dev_id`
- `runtime_status`
- `issue_id`
- `objective`
- `evidence_read`
- `missing_evidence`
- `proposed_change_type`
- `files_likely_to_change`
- `implementation_plan`
- `validation_commands`
- `risks`
- `requires_human_approval`
- `next_safe_actions`

## Runtime statuses

- `builder_plan_ready`
- `missing_issue_id`
- `issue_not_found`
- `missing_evidence`
- `blocked_dirty_worktree`
- `qa_failed`

## Non-goals

- Do not apply patches.
- Do not commit.
- Do not close issues.
- Do not mutate backlog/current-project.
