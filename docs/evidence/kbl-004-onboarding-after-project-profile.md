# KBL-004 Evidence: Onboarding after project profile

Date: 2026-05-29

## Test

Ran Pi from the repository root:

    cd "$HOME/Desktop/Sync/Github Kajiya/kajiya-build-line"
    pi

Then executed:

    /kajiya-onboard

The command prefilled the onboarding prompt. After pressing Enter, Pi inspected the repository in read-only mode.

## Evidence read

The onboarding pi.dev successfully read:

- `.kajiya/project.json`
- `docs/state/current-project.json`
- `docs/state/backlog.json`
- `docs/LLM_HANDOFF_PROTOCOL.md`
- `git status --short`
- `git --no-pager log --oneline -12`

## Result

The onboarding output reported:

- `ok`: true
- `pi_dev_id`: `kajiya_onboard_project`
- `missing_evidence`: []
- `inferred_project_type`: Kajiya-managed project / portable_development_build_line
- active backlog candidate: `KBL-004`

## Interpretation

This confirms that KBL-003 succeeded. The project now has a local `.kajiya/project.json` profile, and onboarding can discover the project without relying on chat memory.

## Next step

Proceed with KBL-004:

- add deterministic `status`
- add deterministic `qa`
- return JSON-compatible output
- prepare for JSON Schema validation
