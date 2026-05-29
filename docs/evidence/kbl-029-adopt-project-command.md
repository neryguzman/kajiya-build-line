# KBL-029 Evidence: read-only adopt-project command

Date: 2026-05-30

## Implemented

Added read-only project adoption inspection command:

    kajiya-build-line adopt-project

## Purpose

Kajiya Build Line can initialize fresh repositories, but mature Kajiya repositories such as kajiya-context-engine already have their own state, backlog, handoff doctrine, schemas, scenarios, and pi.dev governance.

The adopt-project command inspects the current working directory and returns a JSON-compatible adoption plan without modifying files.

## Files added

- `src/kajiya_build_line/adopt_project.py`

## Files updated

- `src/kajiya_build_line/cli.py`

## Behavior

The command detects:

- `.kajiya/project.json`
- `docs/state/current-project.json`
- `docs/state/backlog.json`
- `docs/LLM_HANDOFF_PROTOCOL.md`
- `docs/LLM_ENTRYPOINT.md`
- `AGENTS.md`
- `docs/org-roam`
- `docs/schemas`
- `docs/scenarios`
- `docs/test-scenarios`
- `.pi/extensions`
- `.pi/kajiya`

It classifies repositories as:

- `fresh_repo`
- `already_initialized`
- `mature_kajiya_repo`
- `partial_kajiya_repo`
- `incompatible_repo`

## Safety

The command is read-only.

It does not:

- create files
- modify files
- delete files
- run init-project
- update backlog state
- update current-project state

## Validation

The following passed:

    python -m compileall src
    kajiya-build-line adopt-project
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check

## KCE adoption test

The command was tested against kajiya-context-engine using the Build Line executable from its virtual environment.

Expected KCE outcome:

- mature Kajiya repository detected
- existing current-project/backlog/handoff detected
- AGENTS.md reported missing
- do_not_run_init_project returned true
- adoption plan recommends AGENTS bridge instead of init-project

## Architectural significance

This lets Kajiya Build Line adopt mature Kajiya repositories without overwriting their existing doctrine.

Build Line becomes a portable governance layer, not a repo colonizer.
