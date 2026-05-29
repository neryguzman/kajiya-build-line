# KBL-018 Evidence: AGENTS.md bootstrap and upstream improvement protocol

Date: 2026-05-29

## Implemented

Updated `kajiya-build-line init-project` to create root-level:

    AGENTS.md

## Files updated

- `src/kajiya_build_line/init_project.py`

## AGENTS.md purpose

The generated AGENTS.md gives Pi/coding agents repository-level instructions.

It explains:

- Pi/Pocock is the selected interactive coding-agent runtime.
- Kajiya Build Line is the deterministic project governance layer.
- Project-local files are the source of truth.
- Backlog-first execution is required.
- Evidence should precede task briefs.
- Task briefs should precede Builder work.
- QA and JSON Schema validation are required before issue closure.

## Upstream improvement protocol

AGENTS.md now explains that reusable improvements discovered inside child repositories should not silently fork Kajiya Build Line behavior.

Instead, reusable framework improvements should be proposed back to the main `kajiya-build-line` repository.

Project-specific behavior belongs in the child repository.

Reusable framework behavior belongs upstream.

## Validation

A temporary git repository was initialized.

The command:

    kajiya-build-line init-project --project-id temp-agents-test --project-name "Temp AGENTS Test" --project-type software_project

created AGENTS.md.

Running init-project again in the same temp repo returned:

- `ok`: false
- `runtime_status`: `blocked_existing_files`

This confirms AGENTS.md is protected by the no-overwrite behavior.

Main repository validation passed:

    kajiya-build-line qa
    kajiya-build-line validate-json

## Architectural significance

Bootstrapped repositories now carry agent-facing operating instructions.

This bridges Pi as the coding-agent runtime with Kajiya Build Line as the deterministic project governance layer.

It also creates an explicit upstream contribution loop for improving the main Build Line framework from discoveries made in child repos.
