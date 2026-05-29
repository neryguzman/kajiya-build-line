# KBL-024 Evidence: read-only checkpoint orientation command

Date: 2026-05-30

## Implemented

Added read-only deterministic checkpoint orientation through:

    kajiya-build-line checkpoint

## Files added/updated

- `src/kajiya_build_line/checkpoint.py`
- `src/kajiya_build_line/cli.py`

## Behavior

The checkpoint command is read-only.

It inspects deterministic project and git state, including:

- active issue
- active workstream
- git status --short
- git diff --name-only
- git diff --stat
- latest commit
- QA status
- validate-json status
- active task brief path when present

It returns JSON-compatible output with:

- `schema_version`: `kajiya.checkpoint.v1`
- `kind`: `kajiya_checkpoint`
- `active_issue_id`
- `active_workstream`
- `dirty`
- `changed_files`
- `latest_commit`
- `qa_ok`
- `validation_ok`
- `task_brief_path`
- `recommended_operator_action`
- `next_human_input_contract`

## Validation

The command:

    kajiya-build-line checkpoint

returned:

- `ok`: true
- `active_issue_id`: `KBL-024`
- `active_workstream`: `deterministic_checkpoint_orientation`
- `qa_ok`: true
- `validation_ok`: true
- `task_brief_path`: `docs/task-briefs/KBL-024.json`

Additional validation passed:

    python -m compileall src
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check

## Architectural significance

This clarifies the core Kajiya Build Line boundary:

Everything should be deterministic except the bounded Builder step.

The checkpoint command does not reason, commit, push, or close issues.

Instead, it prepares a deterministic decision packet for the human/operator and advisory chats.

The intended loop is now:

    checkpoint
      -> human/chat decides
      -> add-issue / task-brief / evidence / close-issue
      -> bounded Builder only when code generation is explicitly needed

This prevents Pi or another LLM from inventing strategy while still allowing a Builder to modify code when given a narrow human-authored instruction.
