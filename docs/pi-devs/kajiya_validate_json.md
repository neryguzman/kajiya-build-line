# kajiya_validate_json

## Purpose

Validate durable Kajiya Build Line JSON artifacts against their JSON Schemas.

## Command

    kajiya-build-line validate-json

## Safety

- Read-only.
- No external writes.
- No file modifications.
- No LLM required.

## Validates

- `.kajiya/project.json` against `docs/schemas/kajiya-project.schema.json`
- `docs/task-briefs/KBL-008.json` against `docs/schemas/kajiya-task-brief.schema.json`

## Output

Returns JSON-compatible output with:

- `schema_version`
- `kind`
- `ok`
- `pi_dev_id`
- `runtime_status`
- `validated`
- `next_safe_actions`

## Runtime statuses

- `json_validation_passed`
- `json_validation_failed`
