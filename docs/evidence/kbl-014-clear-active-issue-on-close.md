# KBL-014 Evidence: clear active issue when closing without next issue

Date: 2026-05-29

## Implemented

Updated `kajiya-build-line close-issue` behavior so that closing an issue without `--next-issue-id` clears the active issue state.

## Files updated

- `src/kajiya_build_line/backlog.py`

## Behavior changed

Before:

- Closing an issue without `--next-issue-id` updated `next_recommended_action`.
- But `current-project.json` still retained the closed issue as `active_issue_id`.

After:

- `active_issue_id` is set to `null`.
- `active_workstream` is set to `backlog_selection`.
- `next_recommended_action` remains `Select the next backlog item.`

## Validation

The following commands passed:

    python -m compileall src
    kajiya-build-line qa
    kajiya-build-line validate-json
    kajiya-build-line next

## Architectural significance

The operator cockpit is now consistent after issue closure.

When there is no active issue, `next` and `summary` should no longer report the last closed issue as active.
