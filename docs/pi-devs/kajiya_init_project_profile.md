# kajiya_init_project_profile

## Purpose

Create the project-local identity file used by Kajiya Build Line.

This pi.dev creates:

    .kajiya/project.json

The profile tells onboarding and future build-line steps where to find the backlog, handoff protocol, schemas, evidence, validation commands, runtime policy, memory policy, and safety policy.

## Safety

- Local write only.
- Requires explicit human confirmation.
- Must not store secrets.
- Must not store machine-specific absolute paths.
- Must not include project-specific chat memory.
- Must be portable across computers.

## Input contract

Required:

- `project_id`
- `project_name`
- `project_type`

Optional:

- `canonical_backlog`
- `handoff_protocol`
- `validation_commands`

## Output shape

Return JSON-compatible output with:

- `ok`
- `pi_dev_id`
- `runtime_status`
- `created_files`
- `updated_files`
- `validation_commands`
- `next_safe_actions`

## Runtime statuses

- `project_profile_created`
- `project_profile_exists`
- `blocked_missing_confirmation`
- `schema_validation_failed`

## Next safe actions

After creating the profile:

1. Run `kajiya_onboard_project` again.
2. Run deterministic validation.
3. Continue to the active backlog item.
