# Kajiya Build Line

Kajiya Build Line is a portable development governance layer for Kajiya-style software projects.

It is not an operational product. It is the workshop used to enter any repository, discover its local state, read its backlog, preserve handoff context, guide LLM-assisted development, validate work, and keep git history meaningful.

## Purpose

The goal is to make software work resumable, inspectable, and backlog-governed.

Kajiya Build Line exists because long LLM-assisted programming sessions lose context. Each repository should carry its own local source of truth:

- a project profile
- a canonical backlog
- a current project state file
- a handoff protocol
- validation commands
- git commits as historical evidence

The system should not rely on chat memory. A new Pi/Pocock session, ChatGPT session, coding agent, or human operator should be able to enter a repository, run the onboarding step, read the local files, and know what is safe to do next.

## Core principles

- Backlog before code.
- Handoff before long work.
- Git commits preserve evidence.
- Builder reasoning is bounded.
- QA and validation are deterministic.
- Project memory lives in project files, not in the LLM.
- External writes require explicit human confirmation.
- Kajiya Build Line is portable across repositories.

## Architecture

Kajiya Build Line is designed as a Pi/Pocock-governed build line:

    Pi/Pocock
      -> Kajiya Build Line extension / handler
      -> onboarding pi.dev
      -> backlog selection
      -> builder planning
      -> QA validation
      -> backlog update
      -> handoff update
      -> git commit

The LLM may reason, but the workflow should remain constrained by declared steps, local files, and deterministic validation.

## First pi.dev

The first permanent pi.dev-style station is `kajiya_onboard_project`.

It is read-only. It inspects the current repository and reports:

- project root
- local project profile status
- backlog status
- handoff status
- git status
- recent commits
- missing evidence
- next safe actions

It must not assume the repository is `kajiya-context-engine` or any other specific project.

## Relationship to Kajiya Context Engine

Kajiya Context Engine is an operational cockpit.

Kajiya Build Line is the portable workshop used to build and maintain projects like Kajiya Context Engine.

The product should not carry the workshop inside itself. The workshop enters a project, reads its local state, helps improve it, validates work, and exits.

## Current status

The repository has:

- a Python CLI skeleton
- a local Pi extension
- an onboarding pi.dev document
- initial GitHub remote

The next priority is to formalize the project backlog, handoff protocol, and local project profile.

## Data model policy

Kajiya Build Line uses JSON as the current canonical storage format and JSON Schema as the validation contract.

The long-term design target is Datomic-style migration. Durable records should therefore be shaped as stable, explicit, versioned facts that can later be transformed into entity-attribute-value records.

Every durable JSON record should try to include:

- `schema_version`
- `kind`
- stable id
- `source_of_truth`
- clear timestamps where relevant
- validation schema
- safety metadata where relevant
