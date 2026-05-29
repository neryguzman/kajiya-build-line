# KBL-003 Evidence: Project profile initialization

Date: 2026-05-29

## Action

Created project-local profile:

    .kajiya/project.json

Created JSON Schema:

    docs/schemas/kajiya-project.schema.json

Created pi.dev documentation:

    docs/pi-devs/kajiya_init_project_profile.md

## Architectural note

The project profile is local to this repository and contains no secrets or machine-specific absolute paths.

It declares:

- canonical backlog path
- current-project path
- handoff protocol path
- Pi/Pocock runtime policy
- memory policy
- JSON Schema validation policy
- future Datomic-style migration policy
- safety policy

## Datomic-style principle

Durable JSON records should be shaped so they can later be transformed into entity-attribute-value facts.

The current project profile declares:

- `schema_version`
- `kind`
- `project_id`
- `source_of_truth`
- canonical paths
- policies
- active pi.devs

## Close criteria check

- Init is separate from onboarding: passed.
- Init requires explicit human approval: passed by human-directed command.
- Generated profile contains no machine-specific secrets: passed.
- Profile is portable across computers: passed.
