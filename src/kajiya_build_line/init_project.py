from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build_project_profile(project_id: str, project_name: str, project_type: str) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "schema_version": "kajiya.project.v1",
        "kind": "kajiya_project_profile",
        "project_id": project_id,
        "project_name": project_name,
        "project_type": project_type,
        "created_at": today,
        "updated_at": today,
        "source_of_truth": ".kajiya/project.json",
        "purpose": "Project-local Kajiya Build Line profile for backlog-first, handoff-ready, deterministic project work.",
        "canonical_paths": {
            "backlog": "docs/state/backlog.json",
            "current_project": "docs/state/current-project.json",
            "handoff_protocol": "docs/LLM_HANDOFF_PROTOCOL.md",
            "evidence": "docs/evidence",
            "task_briefs": "docs/task-briefs",
        },
        "runtime": {
            "llm_runtime": "pi_pocock",
            "provider": "configured_in_pi",
            "direct_model_sdk_required": False,
        },
        "memory_policy": {
            "llm_memory": "do_not_rely_on_chat_memory",
            "project_memory": "project_files_only",
            "global_memory": "portable_doctrine_only",
            "project_specific_state_location": "this_repository",
        },
        "data_model_policy": {
            "canonical_format": "json",
            "validation": "json_schema",
            "future_migration_target": "datomic_style_datoms",
        },
        "safety_policy": {
            "onboarding": "read_only",
            "local_writes": "require_explicit_human_confirmation",
            "external_writes": "forbidden_without_specific_confirmed_pi_dev",
        },
    }


def build_backlog(project_id: str) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "schema_version": "kajiya.backlog.v1",
        "project_id": project_id,
        "updated_at": today,
        "source_of_truth": "docs/state/backlog.json",
        "rules": [
            "Backlog is required before meaningful implementation.",
            "Every meaningful code, docs, extension, or workflow change must map to an issue_id.",
            "Builder may reason, but must not modify files without explicit human approval.",
            "QA and validation must be deterministic whenever possible.",
            "Project-specific memory must live in the target project, not globally in Kajiya Build Line.",
        ],
        "items": [],
    }


def build_current_project(project_id: str) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "schema_version": "kajiya.current_project.v1",
        "project_id": project_id,
        "updated_at": today,
        "active_issue_id": None,
        "active_workstream": "backlog_selection",
        "last_completed": [
            "Initialized Kajiya Build Line project-local files."
        ],
        "next_recommended_action": "Create or select the first backlog item.",
        "resume_reading_order": [
            ".kajiya/project.json",
            "docs/state/current-project.json",
            "docs/state/backlog.json",
            "docs/LLM_HANDOFF_PROTOCOL.md",
            "git --no-pager log --oneline -12",
            "git status --short",
        ],
        "validation_commands": [
            "git --no-pager diff --check",
        ],
        "safety_constraints": [
            "Do not rely on chat memory.",
            "Use project-local files as memory.",
            "Local writes require explicit human confirmation.",
        ],
    }


def build_handoff_protocol(project_name: str) -> str:
    return f"""# LLM Handoff Protocol

This file explains how a new ChatGPT, Pi/Pocock session, Manus session, or future agent should resume work on {project_name} safely.

## Required reading order

Do not infer from chat history first.

Read in this order:

1. `.kajiya/project.json`
2. `docs/state/current-project.json`
3. `docs/state/backlog.json`
4. `git --no-pager log --oneline -12`
5. `git status --short`

## Rules

- Backlog before code.
- Handoff before long work.
- Git commits preserve evidence.
- Project memory lives in project files, not in the LLM.
- Do not modify files unless the work maps to a backlog item.
- External writes require explicit human confirmation.
"""


def init_project(
    root: Path,
    project_id: str,
    project_name: str,
    project_type: str,
) -> dict[str, Any]:
    root = root.resolve()

    planned_files = {
        ".kajiya/project.json": build_project_profile(project_id, project_name, project_type),
        "docs/state/backlog.json": build_backlog(project_id),
        "docs/state/current-project.json": build_current_project(project_id),
    }

    planned_text_files = {
        "docs/LLM_HANDOFF_PROTOCOL.md": build_handoff_protocol(project_name),
        "docs/evidence/.gitkeep": "",
        "docs/task-briefs/.gitkeep": "",
    }

    conflicts = [
        rel for rel in [*planned_files.keys(), *planned_text_files.keys()]
        if (root / rel).exists()
    ]

    if conflicts:
        return {
            "schema_version": "kajiya.init_project.v1",
            "kind": "kajiya_init_project",
            "ok": False,
            "pi_dev_id": "kajiya_init_project",
            "runtime_status": "blocked_existing_files",
            "project_root": str(root),
            "conflicts": conflicts,
            "created_files": [],
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": "Refusing to overwrite existing project files.",
                }
            ],
        }

    created_files: list[str] = []

    for rel, payload in planned_files.items():
        write_json(root / rel, payload)
        created_files.append(rel)

    for rel, content in planned_text_files.items():
        write_text(root / rel, content)
        created_files.append(rel)

    return {
        "schema_version": "kajiya.init_project.v1",
        "kind": "kajiya_init_project",
        "ok": True,
        "pi_dev_id": "kajiya_init_project",
        "runtime_status": "project_initialized",
        "project_root": str(root),
        "project_id": project_id,
        "project_name": project_name,
        "project_type": project_type,
        "created_files": created_files,
        "conflicts": [],
        "next_safe_actions": [
            {
                "action": "review_created_files",
                "command": "git status --short",
            },
            {
                "action": "create_first_backlog_item",
                "reason": "Project is initialized but has no backlog items yet.",
            },
        ],
    }
