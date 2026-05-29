from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def add_issue(
    root: Path,
    issue_id: str,
    title: str,
    priority: str,
    issue_type: str,
    problem: str,
    expected_behavior: str,
    proposed_changes: list[str],
    files_likely_to_change: list[str],
    validation_commands: list[str],
    close_criteria: list[str],
    activate: bool = False,
    claimed_by: str = "Nery + ChatGPT",
    branch: str = "main",
) -> dict[str, Any]:
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
            "schema_version": "kajiya.add_issue_result.v1",
            "kind": "kajiya_add_issue_result",
            "ok": False,
            "pi_dev_id": "kajiya_add_issue",
            "runtime_status": "missing_required_files",
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
    today = date.today().isoformat()

    items = backlog.setdefault("items", [])
    existing_ids = {item.get("issue_id") for item in items}

    if issue_id in existing_ids:
        return {
            "schema_version": "kajiya.add_issue_result.v1",
            "kind": "kajiya_add_issue_result",
            "ok": False,
            "pi_dev_id": "kajiya_add_issue",
            "runtime_status": "duplicate_issue_id",
            "issue_id": issue_id,
            "next_safe_actions": [
                {
                    "action": "review_existing_issue",
                    "command": f"kajiya-build-line backlog",
                }
            ],
        }

    item = {
        "issue_id": issue_id,
        "title": title,
        "status": "in_progress" if activate else "todo",
        "priority": priority,
        "type": issue_type,
        "claim_status": "claimed" if activate else "unclaimed",
        "claimed_by": claimed_by if activate else None,
        "branch": branch,
        "problem": problem,
        "expected_behavior": expected_behavior,
        "proposed_change": proposed_changes,
        "files_likely_to_change": files_likely_to_change,
        "validation_commands": validation_commands,
        "close_criteria": close_criteria,
        "created_at": today,
    }

    # Keep the JSON explicit but avoid noisy nulls where possible.
    if item["claimed_by"] is None:
        item.pop("claimed_by")

    items.append(item)
    backlog["updated_at"] = today
    write_json(backlog_path, backlog)

    updated_files = ["docs/state/backlog.json"]

    if activate:
        current["updated_at"] = today
        current["active_issue_id"] = issue_id
        current["active_workstream"] = issue_type
        current["next_recommended_action"] = f"Work on {issue_id}: {title}"
        write_json(current_path, current)
        updated_files.append("docs/state/current-project.json")

    return {
        "schema_version": "kajiya.add_issue_result.v1",
        "kind": "kajiya_add_issue_result",
        "ok": True,
        "pi_dev_id": "kajiya_add_issue",
        "runtime_status": "issue_added",
        "issue_id": issue_id,
        "activated": activate,
        "updated_files": updated_files,
        "next_safe_actions": [
            {
                "action": "review_backlog",
                "command": "kajiya-build-line backlog",
            },
            {
                "action": "run_qa",
                "command": "kajiya-build-line qa",
            },
            {
                "action": "commit",
                "requires_human_approval": True,
            },
        ],
    }
