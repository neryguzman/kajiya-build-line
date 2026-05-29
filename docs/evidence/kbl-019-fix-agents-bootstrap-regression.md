# KBL-019 Evidence: fix AGENTS.md bootstrap regression

Date: 2026-05-29

## Problem found

KBL-018 claimed that `init-project` created root-level `AGENTS.md`.

However, validation in a temporary repository showed:

    head: AGENTS.md: No such file or directory

The `created_files` output also did not include `AGENTS.md`.

This meant the architecture decision was correct, but the implementation was incomplete.

## Root cause

`agents_md(...)` existed in `src/kajiya_build_line/init_project.py`, but `AGENTS.md` was not included in `planned_text_files`.

Therefore the generator existed but was never written during `init-project`.

## Fix implemented

Updated `src/kajiya_build_line/init_project.py` so `planned_text_files` includes:

    "AGENTS.md": agents_md(project_id, project_name, project_type)

## Validation

A fresh temporary git repository was initialized.

The command:

    kajiya-build-line init-project --project-id temp-agents-fix --project-name "Temp AGENTS Fix" --project-type software_project

returned:

- `ok`: true
- `runtime_status`: `project_initialized`

The `created_files` output included:

- `AGENTS.md`

The shell check passed:

    test -f AGENTS.md

The beginning of AGENTS.md was printed successfully and included:

- project_id
- project_name
- project_type
- Pi/Pocock runtime boundary
- Kajiya Build Line deterministic governance rules
- startup flow
- deterministic-first workflow

Running `init-project` a second time returned:

- `ok`: false
- `runtime_status`: `blocked_existing_files`

The `conflicts` output included:

- `AGENTS.md`

Main repository validation passed:

    python -m compileall src
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check

## Architectural significance

Kajiya Build Line now actually bootstraps root-level agent instructions into child repositories.

This makes `init-project` usable as the bridge between:

- Pi/Pocock as coding-agent runtime
- Kajiya Build Line as deterministic project governance
- upstream improvement protocol for reusable framework changes

## Regression lesson

Evidence must match actual command output.

KBL-018 documented the intended behavior, but KBL-019 corrected the implementation and validated the result.
