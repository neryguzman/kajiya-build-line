# LLM Handoff Protocol

This file explains how a new ChatGPT, Pi/Pocock session, Manus session, or future agent should resume work on Kajiya Build Line safely.

## Required reading order

Do not infer from chat history first.

Read in this order:

1. `README.md`
2. `docs/state/current-project.json`
3. `docs/state/backlog.json`
4. `docs/decisions/0001-project-scope.md`
5. `docs/pi-devs/kajiya_onboard_project.md`
6. `git --no-pager log --oneline -12`
7. `git status --short`

## Current principle

Kajiya Build Line is the portable development workshop.

It is not the operational Kajiya Context Engine product.

A project should carry its own state in local files. The LLM should not rely on hidden memory or previous chat context.

## Before modifying files

Report:

- current project
- active issue_id
- latest commit reviewed
- files likely to change
- validation commands
- safety constraints
- whether local writes are approved

If no backlog item maps to the proposed work, stop and create or select a backlog item first.

## Safety

- Onboarding is read-only.
- Project initialization is local-write and requires confirmation.
- Builder is plan-only until explicitly approved.
- QA should be deterministic.
- External writes are forbidden unless a specific confirmed pi.dev exists.

## Normal loop

1. Run or invoke onboarding.
2. Read project files.
3. Select backlog issue.
4. Plan work.
5. Confirm local write if needed.
6. Modify files.
7. Run validation.
8. Commit.
9. Update backlog/current-project.
10. Push.
