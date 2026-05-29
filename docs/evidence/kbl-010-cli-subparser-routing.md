# KBL-010 Evidence: CLI subparser routing

Date: 2026-05-29

## Implemented

Refactored `src/kajiya_build_line/cli.py` to use `argparse.ArgumentParser` with subparsers.

## Commands verified

The following commands executed successfully after the refactor:

- `kajiya-build-line status`
- `kajiya-build-line qa`
- `kajiya-build-line validate-json`
- `kajiya-build-line evidence --read docs/state/backlog.json --list src/kajiya_build_line --grep close_issue --grep-path src --git-log 5`
- `kajiya-build-line task-brief --issue-id KBL-010 --instruction "Refactor CLI routing to argparse subparsers without changing command behavior." --evidence docs/evidence/kbl-009-validate-json-command.md --allowed-file src/kajiya_build_line/cli.py --validation "kajiya-build-line qa"`

## Architectural significance

The CLI no longer relies on fragile hand-written command dispatch.

Each command now registers its parser and handler through one deterministic routing table using argparse subparsers.

This prevents the class of bug where a command appears in usage text but is not actually dispatched.

## Close criteria check

- CLI uses argparse subparsers: passed.
- status command still works: passed.
- qa command still works: passed.
- validate-json command still works: passed.
- evidence command still works: passed.
- task-brief command still works: passed.
- close-issue parser is registered: passed.
- QA passes: passed.
- validate-json passes: passed.
