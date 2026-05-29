# Kajiya Build Line

Use this skill when working on Kajiya-style repositories that require backlog-governed, handoff-ready, deterministic development.

## Core rule

Do not rely on chat memory.

Always inspect the current working directory and local project files before proposing work.

## Required project-local sources

Prefer reading, if present:

1. `.kajiya/project.json`
2. `docs/state/current-project.json`
3. `docs/state/backlog.json`
4. `docs/LLM_HANDOFF_PROTOCOL.md`
5. `git status --short`
6. `git --no-pager log --oneline -12`

## Builder behavior

The Builder may reason, but must return structured plans.

The Builder must not claim files were modified unless a deterministic command actually modified them.

The Builder must not invent project-specific memory.

## Safety

External writes require explicit human confirmation.

Do not expose operational behavior unless it is registered in the project-local governance system.

## Output shape

Prefer JSON-compatible summaries with:

- ok
- runtime_status
- project_root
- evidence_read
- missing_evidence
- proposed_change_type
- files_likely_to_change
- validation_commands
- next_safe_actions
