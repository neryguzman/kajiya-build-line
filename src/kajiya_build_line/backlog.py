from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def close_issue(
    root: Path,
    issue_id: str,
    next_issue_id: str | None,
    evidence: list[str],
    completion_note: str,
    commit: str | None = None,
) -> dict[str, Any]:
    backlog_path = root / "docs" / "state" / "backlog.json"
    current_path = root / "docs" / "state" / "current-project.json"

    if not backlog_path.exists():
        return {
            "schema_version": "kajiya.issue_transition.v1",
            "kind": "kajiya_issue_transition",
            "ok": False,
            "pi_dev_id": "kajiya_issue_transition",
            "runtime_status": "missing_backlog",
            "missing_evidence": ["docs/state/backlog.json"],
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": "Backlog is required before issue transition.",
                }
            ],
        }

    if not current_path.exists():
        return {
            "schema_version": "kajiya.issue_transition.v1",
            "kind": "kajiya_issue_transition",
            "ok": False,
            "pi_dev_id": "kajiya_issue_transition",
            "runtime_status": "missing_current_project",
            "missing_evidence": ["docs/state/current-project.json"],
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": "Current project state is required before issue transition.",
                }
            ],
        }

    backlog = load_json(backlog_path)
    current = load_json(current_path)
    today = date.today().isoformat()

    items = backlog.get("items", [])
    by_id = {item.get("issue_id"): item for item in items}

    if issue_id not in by_id:
        return {
            "schema_version": "kajiya.issue_transition.v1",
            "kind": "kajiya_issue_transition",
            "ok": False,
            "pi_dev_id": "kajiya_issue_transition",
            "runtime_status": "issue_not_found",
            "issue_id": issue_id,
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": f"Issue {issue_id} does not exist in backlog.",
                }
            ],
        }

    if next_issue_id and next_issue_id not in by_id:
        return {
            "schema_version": "kajiya.issue_transition.v1",
            "kind": "kajiya_issue_transition",
            "ok": False,
            "pi_dev_id": "kajiya_issue_transition",
            "runtime_status": "next_issue_not_found",
            "issue_id": issue_id,
            "next_issue_id": next_issue_id,
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": f"Next issue {next_issue_id} does not exist in backlog.",
                }
            ],
        }

    closed = by_id[issue_id]
    closed["status"] = "done"
    closed["completed_at"] = today
    closed["last_activity_commit"] = commit or "pending_commit"
    if evidence:
        existing = closed.get("evidence", [])
        merged = list(dict.fromkeys([*existing, *evidence]))
        closed["evidence"] = merged

    activated = None
    if next_issue_id:
        activated = by_id[next_issue_id]
        activated["status"] = "in_progress"
        activated["claim_status"] = "claimed"
        activated["claimed_by"] = activated.get("claimed_by") or "Nery + ChatGPT"
        activated["branch"] = activated.get("branch") or "main"

    backlog["updated_at"] = today
    write_json(backlog_path, backlog)

    current["updated_at"] = today
    if completion_note:
        current.setdefault("last_completed", []).append(completion_note)

    if next_issue_id and activated:
        current["active_issue_id"] = next_issue_id
        current["active_workstream"] = activated.get("type") or next_issue_id
        current["next_recommended_action"] = (
            f"Work on {next_issue_id}: {activated.get('title', '').strip()}"
        )
    else:
        current["active_issue_id"] = None
        current["active_workstream"] = "backlog_selection"
        current["next_recommended_action"] = "Select the next backlog item."

    write_json(current_path, current)

    updated_files = [
        "docs/state/backlog.json",
        "docs/state/current-project.json",
    ]

    return {
        "schema_version": "kajiya.issue_transition.v1",
        "kind": "kajiya_issue_transition",
        "ok": True,
        "pi_dev_id": "kajiya_issue_transition",
        "runtime_status": "issue_closed",
        "closed_issue_id": issue_id,
        "activated_issue_id": next_issue_id,
        "evidence": evidence,
        "updated_files": updated_files,
        "next_safe_actions": [
            {
                "action": "run_qa",
                "command": "kajiya-build-line qa",
            },
            {
                "action": "review_diff",
                "command": "git --no-pager diff -- docs/state/backlog.json docs/state/current-project.json",
            },
            {
                "action": "commit",
                "requires_human_approval": True,
            },
        ],
    }
