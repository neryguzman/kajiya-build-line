# KBL-017 Evidence: Pi runtime boundary and Build Line differentiation

Date: 2026-05-29

## Implemented

Added architecture decision:

    docs/decisions/0003-pi-runtime-boundary.md

## Decision captured

Pi/Pocock is the selected interactive coding-agent runtime.

Kajiya Build Line is not replacing Pi.

Kajiya Build Line is the deterministic project governance layer above/beside Pi.

## Key boundary

Pi provides:

- coding-agent runtime
- slash commands
- extensions
- skills
- prompt templates
- packages
- model/provider execution
- JSON/RPC integration modes

Kajiya Build Line provides:

- project-local memory
- backlog-first execution
- current project state
- deterministic status
- deterministic QA
- JSON Schema validation
- evidence collection
- human-authored task briefs
- issue transition / close-issue
- bootstrap into another repo
- future Datomic-style modeling

## Regenerative agent boundary

The decision documents that future self-modifying / regenerative agents must operate only through:

- selected backlog issue
- deterministic evidence
- human-authored task brief
- explicit allowed files
- explicit forbidden actions
- deterministic QA
- JSON Schema validation
- diff review
- git commit evidence
- close-issue transition

## Validation

The following passed:

    kajiya-build-line qa
    kajiya-build-line validate-json

## Architectural significance

This decision prevents Kajiya Build Line from drifting into reimplementing Pi.

Pi remains the runtime.

Kajiya Build Line remains the deterministic, schema-governed, project-local memory and execution layer.
