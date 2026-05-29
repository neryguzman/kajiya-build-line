# KBL-027 Evidence: deterministic test scenario artifacts

Date: 2026-05-30

## Implemented

Added durable deterministic test scenario artifacts.

## Files added

- `docs/schemas/kajiya-test-scenario.schema.json`
- `docs/test-scenarios/KBL-025-add-issue-from-json.json`

## Files updated

- `src/kajiya_build_line/validate_json.py`

## Behavior added

`kajiya-build-line validate-json` now validates:

- project profile
- task brief artifacts
- upstream improvement artifacts
- test scenario artifacts under `docs/test-scenarios/*.json`

## First scenario artifact

Added:

    docs/test-scenarios/KBL-025-add-issue-from-json.json

This scenario captures the temp-repo behavior test from KBL-025:

- initialize a temp repo
- create `issue.json`
- run `kajiya-build-line add-issue --from-json issue.json`
- assert first call succeeds
- assert current project activates `TMP-001`
- assert backlog has one item
- assert second call blocks duplicate issue ID

## Validation

The command:

    kajiya-build-line validate-json

validated:

- `.kajiya/project.json`
- `docs/task-briefs/KBL-008.json`
- `docs/upstream-improvements/fix-agents-bootstrap-regression.json`
- `docs/test-scenarios/KBL-025-add-issue-from-json.json`

All returned:

- `ok`: true
- `runtime_status`: `schema_validation_passed`

The QA gate passed:

- `git_diff_check`
- `python_compileall_src`
- `json_schema_validation`

Additional validation passed:

    python -m compileall src
    git --no-pager diff --check

## Commits

    8735c92 Add test scenario artifact validation

Additional architecture documentation was added:

    docs/decisions/0004-human-chat-deterministic-contracts.md
    docs/evidence/kbl-027-human-chat-contract-architecture.md

## Architectural significance

Kajiya Build Line can now store human/chat-designed QA behavior as durable, schema-validated JSON artifacts.

This creates the foundation for a future deterministic test scenario runner.

It also documents the operating boundary:

- humans/chats design QA contracts
- Kajiya CLI validates and eventually executes them
- Builder implements code only when bounded by task briefs
- QA does not invent tests; it executes contracts
