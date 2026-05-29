# KBL-015 Evidence: portable init-project bootstrap

Date: 2026-05-29

## Implemented

Added portable project bootstrap support through:

    kajiya-build-line init-project

## Files added/updated

- `src/kajiya_build_line/init_project.py`
- `src/kajiya_build_line/cli.py`

## Validation

Tested in a temporary git repository created with:

    TMP_REPO="$(mktemp -d)"
    cd "$TMP_REPO"
    git init

The command:

    kajiya-build-line init-project \
      --project-id temp-bootstrap-test \
      --project-name "Temp Bootstrap Test" \
      --project-type software_project

returned:

- `schema_version`: `kajiya.init_project.v1`
- `kind`: `kajiya_init_project`
- `ok`: true
- `runtime_status`: `project_initialized`

## Created files

- `.kajiya/project.json`
- `docs/state/backlog.json`
- `docs/state/current-project.json`
- `docs/LLM_HANDOFF_PROTOCOL.md`
- `docs/evidence/.gitkeep`
- `docs/task-briefs/.gitkeep`

## Safety behavior

Running `init-project` a second time in the same repo returned:

- `ok`: false
- `runtime_status`: `blocked_existing_files`

This confirms the command refuses to overwrite existing project-local Kajiya files by default.

## Main repo validation

The following passed in the Kajiya Build Line repo:

    kajiya-build-line qa
    kajiya-build-line validate-json

## Architectural significance

Kajiya Build Line can now bootstrap its minimal project-local memory structure into another repository.

This is the first major portability milestone.
