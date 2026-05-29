# KBL-026 Evidence: builder context and implement commands

Date: 2026-05-30

## Implemented

Updated the project-local Pi extension:

- `.pi/extensions/kajiya-build-line.ts`

## Commands

Added official context command:

    /kajiya-builder-context

Kept deprecated alias:

    /kajiya-builder-plan

Added bounded implementation launcher:

    /kajiya-builder-implement

## Architectural boundary

Pi commands now separate:

- context preparation
- bounded implementation prompt launching

The human/operator and advisory chats own strategy and planning.

The Builder only implements a human-authored task brief.

## Builder implement boundary

`/kajiya-builder-implement` launches a prompt that instructs the Builder to:

- use `docs/task-briefs/ISSUE_ID.json`
- modify only allowed_files
- obey forbidden_actions
- run validation_commands
- not invent strategy
- not invent roadmap
- not create backlog items
- not commit
- not push
- not close issues

## Validation

The extension was updated, committed, and pushed.

Commit:

    68be252 Add bounded builder implement command

## Reload note

Because this is a Pi extension change, Pi must be reloaded or restarted before the new command appears:

    /reload

Then command completion should show:

    /kajiya-builder-implement
