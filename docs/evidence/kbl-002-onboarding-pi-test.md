# KBL-002 Evidence: kajiya_onboard_project Pi test

Date: 2026-05-29

## Test

Ran Pi from the repository root:

    cd "$HOME/Desktop/Sync/Github Kajiya/kajiya-build-line"
    pi

Then executed the local extension command:

    /kajiya-onboard

The command prefilled the onboarding prompt in the Pi editor. After pressing Enter, Pi executed read-only evidence gathering.

## Observed behavior

Pi loaded the local extension:

    [Extensions]
      kajiya-build-line.ts

The onboarding pi.dev inspected:

- `.kajiya/project.json`
- `docs/state/current-project.json`
- `docs/state/backlog.json`
- `docs/LLM_HANDOFF_PROTOCOL.md`
- `git status --short`
- `git --no-pager log --oneline -12`

## Result

The onboarding station returned JSON-compatible output with:

- `pi_dev_id`: `kajiya_onboard_project`
- `runtime_status`: partially onboarded
- `missing_evidence`: `.kajiya/project.json`
- `active_backlog_candidates`: `KBL-002`, `KBL-003`, `KBL-004`, `KBL-005`
- `next_safe_actions`: recommend `kajiya_init_project_profile` / `KBL-003`

## Close criteria check

- Pi loads the extension: passed.
- `/kajiya-onboard` executes successfully: passed.
- The onboarding prompt does not assume any specific project: passed.
- The station is read-only: passed.

## Notes

The prompt is currently prefilled via `ctx.ui.setEditorText`, requiring the operator to press Enter. This is acceptable for v0.1 because it keeps the operator in control and avoids relying on unstable automatic message injection behavior.
