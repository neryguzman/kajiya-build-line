# KBL-006 Evidence: deterministic issue transition command

Date: 2026-05-29

## Implemented

Added deterministic backlog transition support through:

    kajiya-build-line close-issue

## Files added/updated

- `src/kajiya_build_line/backlog.py`
- `src/kajiya_build_line/cli.py`
- `docs/pi-devs/kajiya_issue_transition.md`
- `docs/schemas/kajiya-issue-transition.schema.json`

## Validation

The following commands passed:

    python -m compileall src
    kajiya-build-line status
    kajiya-build-line qa
    git --no-pager diff --check

## Result

Kajiya Build Line can now close an issue, attach evidence, activate the next issue, and update `docs/state/backlog.json` plus `docs/state/current-project.json` without ad-hoc pasted Python snippets.

## Architectural significance

This moves issue transitions from manual scripting into a repeatable deterministic pi.dev-style command.
