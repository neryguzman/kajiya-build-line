# Evidence: human/chat contract architecture lesson

Date: 2026-05-30

## Observation

During KBL-027, the Pi Builder prompt attempted to implement test scenario artifacts but failed with an unknown error before writing files.

The task was then completed more reliably through direct deterministic shell commands:

- create JSON Schema
- create first test scenario artifact
- update validate-json
- run compile/QA/validation/diff checks
- commit

## Lesson

Long Builder prompts are not the right tool for every task.

For structured JSON/schema/doc artifacts, human/chat can design the content and apply it directly through deterministic shell commands.

Builder should be reserved for bounded source-code implementation where code-generation context is useful.

## Confirmed direction

Kajiya Build Line should formalize:

- human/chat owns contract design
- Pi/CLI owns deterministic execution
- Builder owns bounded code mutation
- QA owns deterministic verification
- JSON Schema owns artifact structure
- commits preserve breadcrumbs

## Related decision

- `docs/decisions/0004-human-chat-deterministic-contracts.md`
