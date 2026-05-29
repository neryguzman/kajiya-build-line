# KBL-025 Evidence: add-issue JSON input support

Date: 2026-05-30

## Implemented

Added JSON file input support to:

    kajiya-build-line add-issue --from-json FILE

## Files updated

- `src/kajiya_build_line/add_issue.py`
- `src/kajiya_build_line/cli.py`

## Builder cycle

The bounded Builder was invoked through:

    /kajiya-builder-implement issue_id=KBL-025

The Builder modified only the allowed implementation files:

- `src/kajiya_build_line/add_issue.py`
- `src/kajiya_build_line/cli.py`

The Builder ran:

- `python -m compileall src`
- `kajiya-build-line add-issue --help`
- `kajiya-build-line qa`
- `kajiya-build-line validate-json`
- `git --no-pager diff --check`

The Builder did not commit, push, or close the issue.

## Human review correction

Initial implementation added `--from-json`, but the first real temp-repo test failed because argparse still required:

- `--issue-id`
- `--title`
- `--priority`
- `--type`
- `--problem`
- `--expected-behavior`

That prevented `--from-json` from being used alone.

The fix moved required-field enforcement out of argparse and into the deterministic `add_issue()` function, where JSON and CLI fields can be merged before validation.

## Behavior verified

A fresh temporary git repository was initialized with:

    kajiya-build-line init-project \
      --project-id temp-from-json-test \
      --project-name "Temp From JSON Test" \
      --project-type software_project

Then a JSON issue file was created with:

- `issue_id`: `TMP-001`
- `title`: `Temp issue from JSON`
- `priority`: `P0`
- `type`: `test`
- `problem`
- `expected_behavior`
- `proposed_change`
- `files_likely_to_change`
- `validation_commands`
- `close_criteria`
- `activate`: true

The command:

    kajiya-build-line add-issue --from-json issue.json

returned:

- `ok`: true
- `runtime_status`: `issue_added`
- `issue_id`: `TMP-001`
- `activated`: true

The temp repo current-project state showed:

- `active_issue_id`: `TMP-001`
- `active_workstream`: `test`
- `next_recommended_action`: `Work on TMP-001: Temp issue from JSON`

The temp repo backlog showed:

- `items_count`: 1
- first item issue_id: `TMP-001`
- first item status: `in_progress`

Running the same command again returned:

- `ok`: false
- `runtime_status`: `duplicate_issue_id`
- `issue_id`: `TMP-001`

## Main repo validation

The following passed in the main repo:

    python -m compileall src
    kajiya-build-line add-issue --help
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check

## Commit

    e655d50 Support add-issue from JSON input

## Architectural significance

Kajiya Build Line can now receive structured backlog items from a JSON file.

This completes the intended human/chat + deterministic CLI loop:

    checkpoint
      -> human/chat decides the next issue
      -> human/chat creates structured JSON
      -> add-issue --from-json applies it deterministically
      -> QA and JSON Schema validation protect the repo

This reduces long CLI argument lists and avoids Python heredocs for complex backlog creation.
