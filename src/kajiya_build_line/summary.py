from __future__ import annotations

from pathlib import Path
from typing import Any

from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.validate_json import build_validation_payload


def build_summary_payload(start: Path | None = None) -> dict[str, Any]:
    root = (start or Path.cwd()).resolve()

    status_payload = build_status_payload(root)
    qa_payload = build_qa_payload(root)
    validation_payload = build_validation_payload(root)

    current_project = status_payload.get("current_project") or {}
    backlog_summary = status_payload.get("backlog_summary") or {}
    git = status_payload.get("git") or {}

    active_candidates = backlog_summary.get("active_candidates") or []
    active_issue_id = current_project.get("active_issue_id")

    return {
        "schema_version": "kajiya.summary.v1",
        "kind": "kajiya_summary",
        "ok": bool(
            status_payload.get("ok")
            and qa_payload.get("ok")
            and validation_payload.get("ok")
        ),
        "pi_dev_id": "kajiya_summary",
        "runtime_status": "summary_ready",
        "project_root": str(root),
        "project_id": current_project.get("project_id") or status_payload.get("project_profile", {}).get("project_id"),
        "active_issue_id": active_issue_id,
        "active_workstream": current_project.get("active_workstream"),
        "next_recommended_action": current_project.get("next_recommended_action"),
        "dirty": bool(git.get("dirty")),
        "qa": {
            "ok": bool(qa_payload.get("ok")),
            "runtime_status": qa_payload.get("runtime_status"),
            "checks": [
                {
                    "name": check.get("name"),
                    "ok": bool(check.get("ok")),
                    "runtime_status": check.get("runtime_status"),
                }
                for check in qa_payload.get("checks", [])
            ],
        },
        "validation": {
            "ok": bool(validation_payload.get("ok")),
            "runtime_status": validation_payload.get("runtime_status"),
            "validated_count": len(validation_payload.get("validated", [])),
        },
        "backlog": {
            "counts_by_status": backlog_summary.get("counts_by_status", {}),
            "active_candidates": active_candidates,
        },
        "next_safe_actions": [
            {
                "action": "continue_active_issue" if active_issue_id else "select_backlog_item",
                "issue_id": active_issue_id,
                "reason": current_project.get("next_recommended_action") or "Select the next backlog item.",
            }
        ],
    }
