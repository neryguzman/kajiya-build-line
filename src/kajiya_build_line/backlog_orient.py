from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_backlog_orientation_payload(root: Path) -> dict[str, Any]:
    root = root.resolve()

    backlog_path = root / "docs" / "state" / "backlog.json"
    current_path = root / "docs" / "state" / "current-project.json"

    missing = []
    if not backlog_path.exists():
        missing.append("docs/state/backlog.json")
    if not current_path.exists():
        missing.append("docs/state/current-project.json")

    if missing:
        return {
            "schema_version": "kajiya.backlog_orientation.v1",
            "kind": "kajiya_backlog_orientation",
            "ok": False,
            "pi_dev_id": "kajiya_backlog_orientation",
            "runtime_status": "missing_required_files",
            "project_root": str(root),
            "missing": missing,
            "next_safe_actions": [
                {
                    "action": "bootstrap_check",
                    "command": "kajiya-build-line bootstrap-check",
                }
            ],
        }

    backlog = load_json(backlog_path)
    current = load_json(current_path)

    items = backlog.get("items", [])
    counts = Counter(item.get("status", "unknown") for item in items)

    in_progress_items = [
        {
            "issue_id": item.get("issue_id"),
            "title": item.get("title"),
            "priority": item.get("priority"),
            "type": item.get("type"),
            "status": item.get("status"),
        }
        for item in items
        if item.get("status") == "in_progress"
    ]

    open_items = [
        {
            "issue_id": item.get("issue_id"),
            "title": item.get("title"),
            "priority": item.get("priority"),
            "type": item.get("type"),
            "status": item.get("status"),
        }
        for item in items
        if item.get("status") not in {"done", "in_progress"}
    ]

    active_issue_id = current.get("active_issue_id")
    active_workstream = current.get("active_workstream")
    last_completed = current.get("last_completed", [])

    if active_issue_id:
        recommended_action = current.get("next_recommended_action") or f"Continue active issue {active_issue_id}."
        action = "continue_active_issue"
    else:
        recommended_action = "Create or select the next backlog item."
        action = "select_or_create_backlog_item"

    return {
        "schema_version": "kajiya.backlog_orientation.v1",
        "kind": "kajiya_backlog_orientation",
        "ok": True,
        "pi_dev_id": "kajiya_backlog_orientation",
        "runtime_status": "backlog_orientation_ready",
        "project_root": str(root),
        "project_id": backlog.get("project_id") or current.get("project_id"),
        "active_issue_id": active_issue_id,
        "active_workstream": active_workstream,
        "backlog_counts": dict(counts),
        "in_progress_items": in_progress_items,
        "open_items": open_items,
        "last_completed_tail": last_completed[-8:],
        "next_recommended_action": current.get("next_recommended_action"),
        "recommended_operator_action": recommended_action,
        "resume_reading_order": current.get("resume_reading_order", []),
        "strategic_breadcrumbs": [
            "Pi/Pocock is the selected coding-agent runtime.",
            "Kajiya Build Line is the deterministic project governance layer.",
            "Do not ask Pi to invent strategy or roadmap from memory.",
            "Evidence is for humans and operator review.",
            "Task briefs are human-authored instructions for Builder.",
            "Reusable framework improvements belong upstream.",
            "Durable JSON artifacts should be schema validated.",
            "Project memory lives in repository files, not chat memory.",
        ],
        "builder_instruction_mode": {
            "do_not_ask_pi_to_reason_strategy": True,
            "do_not_ask_pi_to_invent_backlog_items": True,
            "use_pi_for_repo_orientation_or_bounded_builder_execution": True,
            "next_builder_prompt_should_be_human_authored": True,
            "preferred_pi_command": "/kajiya-build-backlog",
            "deterministic_source_command": "kajiya-build-line backlog",
        },
        "safe_commands": [
            "kajiya-build-line backlog",
            "kajiya-build-line next",
            "kajiya-build-line summary",
            "kajiya-build-line qa",
            "kajiya-build-line validate-json",
            "git status --short",
        ],
        "next_safe_actions": [
            {
                "action": action,
                "allowed": True,
                "reason": recommended_action,
            }
        ],
    }
