# Decision 0003: Pi is the coding agent runtime; Kajiya Build Line is the deterministic project governance layer

Date: 2026-05-29

## Decision

Kajiya Build Line will use Pi/Pocock as the primary interactive coding-agent runtime.

Kajiya Build Line is not intended to replace Pi.

Instead, Kajiya Build Line sits above and beside Pi as a deterministic project governance layer.

## Why this exists

Pi already provides a strong coding-agent harness:

- interactive terminal coding agent runtime
- slash commands
- TypeScript extensions
- skills
- prompt templates
- packages
- model/provider configuration
- JSON/RPC integration modes

These features make Pi a good runtime for interactive coding and agent-assisted development.

However, Kajiya Build Line solves a different problem.

Kajiya Build Line exists because long LLM-assisted development sessions lose context, drift across repositories, invent shell commands, and rely too much on hidden chat memory.

The goal is to make every project carry its own durable, auditable, deterministic source of truth.

## Boundary

### Pi provides

Pi is the agent runtime.

It is responsible for:

- interactive coding sessions
- model/provider execution
- extensions
- skills
- prompt templates
- slash command UX
- agent reasoning
- optional JSON/RPC integration
- future self-extension patterns

### Kajiya Build Line provides

Kajiya Build Line is the project governance layer.

It is responsible for:

- project-local memory
- backlog-first execution
- current project state
- deterministic status
- deterministic QA
- JSON Schema validation
- evidence collection
- human-authored task briefs
- issue transition / close-issue
- bootstrap into another repository
- portable handoff protocol
- future Datomic-style modeling

## Deterministic first, LLM second

Kajiya Build Line should prefer deterministic commands whenever possible.

Examples:

- `kajiya-build-line next`
- `kajiya-build-line summary`
- `kajiya-build-line status`
- `kajiya-build-line qa`
- `kajiya-build-line validate-json`
- `kajiya-build-line evidence`
- `kajiya-build-line task-brief`
- `kajiya-build-line close-issue`
- `kajiya-build-line init-project`
- `kajiya-build-line bootstrap-check`

The LLM should be invoked only after the project has produced bounded, project-local, deterministic context.

The LLM should not be asked to rediscover the entire repo every time.

The operator should use deterministic evidence to create a surgical task brief, then pass that task brief to Pi or another coding agent.

## Human-authored task brief

Raw evidence is for the operator.

Task briefs are for the Builder.

The intended flow is:

    operator intent
      -> deterministic evidence collection
      -> human reviews evidence
      -> human writes surgical task brief
      -> Pi/Builder reasons over task brief
      -> allowed files only
      -> QA
      -> JSON Schema validation
      -> diff review
      -> git commit
      -> close issue

This prevents context stuffing and keeps the Builder focused.

## Regenerative agents / self-modifying lambdas

Kajiya Build Line may eventually support regenerative agents: small bounded agentic units that can propose or modify their own code.

This is allowed only under strict constraints.

A regenerative agent must not freely rewrite itself.

It must operate through:

- selected backlog issue
- deterministic evidence
- human-authored task brief
- explicit allowed files
- explicit forbidden actions
- JSON-compatible plan or patch output
- deterministic QA
- JSON Schema validation
- diff review
- git commit evidence
- close-issue transition

The agent may reason.

The deterministic layer decides whether the project state is valid.

## Pi skills, prompts, and extensions

Kajiya Build Line should use Pi-native features where they fit.

Recommended mapping:

    Pi extension
      -> UX shortcuts, slash commands, prompt launchers, permission gates

    Pi prompt templates
      -> simple reusable prompts

    Pi skills
      -> reusable workflows and reference documentation

    Kajiya Build Line Python CLI
      -> deterministic state, QA, validation, evidence, backlog, bootstrap

The Pi extension should not become the main project-state engine.

The Python CLI remains the deterministic source of operational truth.

## Datomic-style modeling rationale

Kajiya Build Line uses JSON and JSON Schema now, but records should be designed so they can later migrate toward a Datomic-style fact model.

Durable records should therefore prefer:

- stable IDs
- explicit `schema_version`
- explicit `kind`
- appendable evidence
- traceable state transitions
- entity-friendly fields
- normalized references where practical

This matters because future agents should be able to query project memory as facts rather than ingesting long text blobs.

The long-term goal is not just documentation.

The long-term goal is agent-safe memory.

## Consequences

- Pi remains the selected coding-agent runtime.
- Kajiya Build Line does not compete with Pi.
- Kajiya Build Line should avoid reimplementing Pi's skill/prompt/extension system.
- Kajiya Build Line owns deterministic project-local state.
- Self-modification is allowed only through bounded workflows.
- JSON Schema is mandatory for durable JSON artifacts.
- Future work should integrate Pi-native prompts/skills where useful, but keep canonical project memory in repository files.
