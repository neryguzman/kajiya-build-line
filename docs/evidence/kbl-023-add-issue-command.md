# KBL-023 Evidence: deterministic add-issue command

Date: 2026-05-29

## Implemented

Added deterministic backlog issue creation through:

    kajiya-build-line add-issue

## Files added/updated

- `src/kajiya_build_line/add_issue.py`
- `src/kajiya_build_line/cli.py`

## Validation

The command exists and exposes:

    kajiya-build-line add-issue --help

Supported fields include:

- `--issue-id`
- `--title`
- `--priority`
- `--type`
- `--problem`
- `--expected-behavior`
- `--proposed-change`
- `--file`
- `--validation`
- `--close-criterion`
- `--activate`

## Real workflow proof

The command was used to create and activate a real backlog item:

    KBL-024 — Add deterministic checkpoint commit and push command

The command returned:

- `schema_version`: `kajiya.add_issue_result.v1`
- `kind`: `kajiya_add_issue_result`
- `ok`: true
- `runtime_status`: `issue_added`
- `issue_id`: `KBL-024`
- `activated`: true

It updated:

- `docs/state/backlog.json`
- `docs/state/current-project.json`

The resulting commit was:

    45737d1 Add and activate checkpoint command workstream using add-issue

## Architectural significance

Kajiya Build Line can now create backlog items without pasted Python heredocs.

This enables the intended workflow:

    Pi/orientation output
      -> human + ChatGPT reason
      -> ChatGPT shapes clean command arguments
      -> kajiya-build-line add-issue writes deterministic JSON state
      -> QA / validation
      -> git commit breadcrumb

This keeps strategy with the human/operator and advisory chats, while Pi/Build Line performs deterministic state transitions.
