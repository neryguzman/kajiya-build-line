# Decision 0004: Human/chat owns contract design; deterministic CLI owns execution

Date: 2026-05-30

## Status

Accepted.

## Context

Kajiya Build Line is repo-agnostic project governance infrastructure.

It is designed to work across repositories without relying on chat memory, hidden LLM state, or project-specific assumptions.

During KBL-025 and KBL-027, we tested the interaction between:

- human/operator
- advisory ChatGPT session
- Pi extension commands
- bounded Builder prompts
- deterministic Kajiya CLI commands
- JSON Schema validation
- QA gates

The important result was that the most reliable flow was not to make Pi reason over long prompts.

The reliable flow was:

1. Human/chat defines intent.
2. Human/chat designs exact QA expectations.
3. Kajiya CLI records intent as JSON artifacts.
4. JSON Schema validates artifact structure.
5. Builder is used only for bounded implementation work.
6. QA executes deterministic contracts.
7. Failures return as structured packets for either Builder retry or human/chat escalation.

## Decision

Kajiya Build Line will prefer deterministic JSON-contract workflows over long freeform prompts.

Humans and advisory chats own:

- strategic reasoning
- backlog priority
- task decomposition
- QA design
- test scenario design
- allowed files
- forbidden actions
- retry/escalation decisions

Kajiya CLI owns:

- deterministic state transitions
- project-local memory
- schema validation
- evidence files
- task briefs
- test scenario artifacts
- checkpoint packets
- QA execution gates
- close-issue transitions

Pi owns:

- interactive runtime
- extension commands
- bounded Builder launchers
- repo-local prompt/context helpers

Builder owns:

- code mutation only
- only within allowed_files
- only from a human-authored task brief
- no commit
- no push
- no close-issue

QA owns:

- deterministic execution of validation commands
- deterministic execution of test scenario contracts when available
- pass/fail output
- failure packets

## Operating rule

Use direct deterministic shell/CLI commands when the task is mostly:

- creating JSON artifacts
- creating JSON Schemas
- updating validation pair lists
- writing evidence files
- updating project state through Kajiya CLI
- running QA
- running temp-repo behavior tests

Use Pi Builder only when the task is mostly:

- editing source code
- refactoring code
- implementing logic across allowed_files
- fixing a failure packet
- applying a bounded change that benefits from coding-agent context

## Prompt-length rule

Avoid long prompts to Pi Builder.

Prefer:

- JSON task brief
- JSON test scenario
- concise Builder instruction
- allowed_files
- validation_commands
- failure packet if retrying

The Builder prompt should point to structured artifacts rather than contain the full reasoning.

## QA design rule

QA does not invent what to test.

Human/chat designs the QA contract.

The QA contract should be stored as durable project-local artifacts, such as:

- `docs/test-scenarios/*.json`
- future `docs/qa-contracts/*.json`
- future failure packets

The deterministic QA runner should execute those artifacts and report results.

## Retry rule

Future repair loops must be bounded.

Recommended default:

1. Builder attempt.
2. QA run.
3. If QA fails, create failure packet.
4. Builder retry 1 using failure packet.
5. QA run.
6. Builder retry 2 if needed.
7. If still failing, escalate to human/chat.

No infinite loops.

## Repo-agnostic rationale

This design works across repositories because project intelligence is externalized into durable contracts:

- backlog items
- task briefs
- evidence files
- test scenarios
- schemas
- checkpoints
- commits

The repo does not need to think.

The repo needs to validate and preserve contracts.

## Consequences

- Kajiya Build Line remains deterministic-first.
- Pi remains the coding-agent runtime, not the strategic planner.
- Builder is allowed to code, but only inside bounded contracts.
- QA becomes contract-driven instead of generic.
- Human/chat remains responsible for judgment.
- JSON Schema becomes the central medium for safe agent-to-agent handoff.
