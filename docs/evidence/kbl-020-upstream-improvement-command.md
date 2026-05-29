# KBL-020 Evidence: upstream improvement proposal command

Date: 2026-05-29

## Implemented

Added deterministic upstream improvement proposal support through:

    kajiya-build-line upstream-improvement

## Files added/updated

- `src/kajiya_build_line/upstream_improvement.py`
- `src/kajiya_build_line/cli.py`
- `docs/upstream-improvements/fix-agents-bootstrap-regression.json`

## Behavior

The command creates proposal artifacts under:

    docs/upstream-improvements/SLUG.json

The proposal records:

- source project
- target project
- title
- problem
- recommendation
- evidence references
- suggested target files
- validation commands
- next steps for upstreaming

## Validation

The command:

    kajiya-build-line upstream-improvement --title "Fix AGENTS bootstrap regression" --source-project kajiya-build-line --problem "init-project had AGENTS generator but did not write AGENTS.md" --recommendation "Add AGENTS.md to planned_text_files and validate in temp repo" --evidence docs/evidence/kbl-019-fix-agents-bootstrap-regression.md --target-file src/kajiya_build_line/init_project.py --validation "kajiya-build-line qa"

returned:

- `ok`: true
- `runtime_status`: `upstream_improvement_created`
- `proposal_path`: `docs/upstream-improvements/fix-agents-bootstrap-regression.json`

Running the same command again returned:

- `ok`: false
- `runtime_status`: `blocked_existing_proposal`

This confirms proposal artifacts are protected from accidental overwrite.

Additional validation passed:

    kajiya-build-line qa
    kajiya-build-line validate-json
    git --no-pager diff --check
    python -m compileall src

## Architectural significance

Kajiya Build Line now has a formal upstream feedback loop.

Child repositories can record reusable framework improvements as durable proposal artifacts instead of silently forking behavior.

This supports the intended pattern:

    child repo discovers reusable improvement
      -> upstream-improvement proposal artifact
      -> main kajiya-build-line backlog/task brief
      -> upstream implementation
      -> QA / validate-json
      -> merge
      -> child repos update behavior

## Notes

This first implementation does not yet add JSON Schema validation for upstream improvement artifacts.

A follow-up backlog item should add a schema and include upstream improvement proposals in `validate-json`.
