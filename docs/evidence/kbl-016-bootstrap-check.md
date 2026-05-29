# KBL-016 Evidence: bootstrap-check command

Date: 2026-05-29

## Implemented

Added read-only repository readiness detection through:

    kajiya-build-line bootstrap-check

## Files added/updated

- `src/kajiya_build_line/bootstrap_check.py`
- `src/kajiya_build_line/cli.py`

## Behavior

In an initialized Kajiya Build Line repository, the command returns:

- `ok`: true
- `initialized`: true
- `runtime_status`: `initialized`
- `missing`: []

In an uninitialized temporary git repository, the command reports missing required Kajiya Build Line files and recommends running `init-project`.

## Bug fixed

Initial implementation treated `docs/evidence/.gitkeep` and `docs/task-briefs/.gitkeep` as required files.

This created a false negative in repositories where those directories existed and contained real files but no `.gitkeep`.

The command now treats the directories as initialized when the directories exist:

- `docs/evidence`
- `docs/task-briefs`

## Validation

The following commands passed:

    kajiya-build-line bootstrap-check
    kajiya-build-line qa
    kajiya-build-line validate-json
    python -m compileall src
    git --no-pager diff --check

## Architectural significance

Kajiya Build Line now has a safe read-only gate before bootstrapping another repository.

The operator can inspect whether a repo needs `init-project` before creating any project-local files.
