# Decision 0001: Kajiya Build Line is separate from Kajiya Context Engine

Date: 2026-05-29

## Decision

Kajiya Build Line will live in its own repository:

    https://github.com/neryguzman/kajiya-build-line

It will not be embedded as a development subsystem inside `kajiya-context-engine`.

## Reason

Kajiya Context Engine is an operational cockpit for emails, projects, CRM mirrors, quote workflows, provider handoff, and outbox governance.

Kajiya Build Line is the portable development workshop used to enter any repository, read local state, enforce backlog-first work, guide Pi/Pocock-based builder reasoning, run deterministic QA, and preserve handoff context.

Managers and operators using Kajiya Context Engine should not need development build-line internals.

## Consequences

- Kajiya Build Line must be project-agnostic.
- It must not assume the current repo is Kajiya Context Engine.
- It may be invoked from any repo via Pi/Pocock or a CLI.
- Project-specific memory must live in the target project.
- The Build Line may read and modify a target project only through explicit backlog-governed steps.
