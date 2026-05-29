# KBL-028 Evidence: deterministic test scenario runner

Date: 2026-05-30

## Implemented

Added deterministic test scenario runner.

## Files added

- `src/kajiya_build_line/run_scenario.py`

## Files updated

- `src/kajiya_build_line/cli.py`

## Command added

    kajiya-build-line run-scenario --scenario FILE

## Scenario executed

The command was tested against:

    docs/test-scenarios/KBL-025-add-issue-from-json.json

This scenario verifies the KBL-025 behavior:

- create isolated temporary workspace
- initialize a temp git repository
- initialize Kajiya Build Line project files
- write `issue.json`
- run `kajiya-build-line add-issue --from-json issue.json`
- inspect current-project state
- inspect backlog state
- run duplicate add-issue command
- assert duplicate issue ID is blocked

## Result

The runner returned:

- `ok`: true
- `runtime_status`: `scenario_passed`
- `scenario_id`: `add_issue_from_json_temp_repo`
- `issue_id`: `KBL-025`

All assertions passed:

- first add-issue call returned `ok: true`
- first add-issue call returned `runtime_status: issue_added`
- current-project activated `TMP-001`
- backlog contained exactly one item
- duplicate add-issue call returned `runtime_status: duplicate_issue_id`

## Important QA rule discovered

A scenario command may return a non-zero exit code and still be part of a passing scenario when the non-zero behavior is expected and asserted.

In this scenario, the duplicate add-issue command returns failure semantics because duplicate issue IDs are correctly blocked.

The runner therefore treats setup commands as required to succeed, while main scenario commands are judged by assertions.

## Validation

The following commands passed:

    python -m compileall src
    kajiya-build-line run-scenario --scenario docs/test-scenarios/KBL-025-add-issue-from-json.json
    kajiya-build-line validate-json
    kajiya-build-line qa
    git --no-pager diff --check

## Commit

    b52c86d Add deterministic test scenario runner

## Architectural significance

Kajiya Build Line can now execute human/chat-designed QA contracts deterministically.

This closes the first loop:

    human/chat designs scenario JSON
      -> JSON Schema validates scenario
      -> run-scenario executes scenario
      -> assertions determine pass/fail
      -> output is JSON-compatible

This creates the base for future QA integration and failure packets.
