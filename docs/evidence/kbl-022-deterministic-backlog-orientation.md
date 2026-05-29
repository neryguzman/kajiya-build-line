# KBL-022 Evidence: deterministic backlog orientation command

Date: 2026-05-29

## Implemented

Added deterministic backlog orientation support through:

    kajiya-build-line backlog

## Files added/updated

- `src/kajiya_build_line/backlog_orient.py`
- `src/kajiya_build_line/cli.py`

## Behavior

The command reads:

- `docs/state/backlog.json`
- `docs/state/current-project.json`

and returns compact JSON-compatible orientation output.

It does not modify project state.

## Validation

The command:

    kajiya-build-line backlog

returned:

- `schema_version`: `kajiya.backlog_orientation.v1`
- `kind`: `kajiya_backlog_orientation`
- `ok`: true
- `runtime_status`: `backlog_orientation_ready`
- `active_issue_id`: `KBL-022`
- `active_workstream`: `deterministic_backlog_orientation`

The output included:

- backlog counts
- in-progress items
- open items
- last completed tail
- resume reading order
- strategic breadcrumbs
- safe commands
- next safe actions

The output also explicitly instructed:

- do not ask Pi to reason strategy
- do not ask Pi to invent backlog items
- use Pi for repo orientation or bounded builder execution
- next Builder prompt should be human-authored
- preferred Pi command: `/kajiya-build-backlog`
- deterministic source command: `kajiya-build-line backlog`

Additional validation passed:

    kajiya-build-line next
    kajiya-build-line summary
    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

This command corrects the operator flow.

Pi should not be asked to invent strategy or recommend roadmap items from memory.

Instead, Pi should use deterministic project-local orientation:

    /kajiya-build-backlog
      -> kajiya-build-line backlog

This lets any future ChatGPT, Pi session, or coding agent reconstruct:

- where the repo is
- what issue is active
- what was recently completed
- what documents to read
- what deterministic commands are safe
- what kind of Builder instruction should come next

The strategy remains with the human/operator and surrounding advisory chats.

The deterministic layer provides breadcrumbs, not invention.
