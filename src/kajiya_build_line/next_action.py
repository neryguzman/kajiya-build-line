from __future__ import annotations

from pathlib import Path
from typing import Any

from kajiya_build_line.summary import build_summary_payload


def build_next_payload(start: Path | None = None) -> dict[str, Any]:
    root = (start or Path.cwd()).resolve()
    summary = build_summary_payload(root)

    active_issue_id = summary.get("active_issue_id")
    dirty = bool(summary.get("dirty"))
    qa_ok = bool((summary.get("qa") or {}).get("ok"))
    validation_ok = bool((summary.get("validation") or {}).get("ok"))
    active_candidates = (summary.get("backlog") or {}).get("active_candidates", [])

    ready_for_next_decision = (
        not active_issue_id
        and not dirty
        and qa_ok
        and validation_ok
    )

    if dirty:
        recommended_action = "Review or commit current working tree changes before selecting another backlog item."
    elif active_issue_id:
        recommended_action = summary.get("next_recommended_action") or f"Continue active issue {active_issue_id}."
    elif ready_for_next_decision:
        recommended_action = "Select or create the next backlog item."
    else:
        recommended_action = "Run QA and validation, then review summary."

    return {
        "schema_version": "kajiya.next.v1",
        "kind": "kajiya_next",
        "ok": bool(summary.get("ok")),
        "pi_dev_id": "kajiya_next",
        "runtime_status": "next_ready",
        "project_root": str(root),
        "active_issue_id": active_issue_id,
        "active_workstream": summary.get("active_workstream"),
        "dirty": dirty,
        "qa_ok": qa_ok,
        "validation_ok": validation_ok,
        "ready_for_next_backlog_decision": ready_for_next_decision,
        "recommended_action": recommended_action,
        "active_candidates": active_candidates,
        "safe_commands": [
            "kajiya-build-line summary",
            "kajiya-build-line qa",
            "kajiya-build-line validate-json",
            "git status --short",
        ],
        "next_safe_actions": [
            {
                "action": "continue_active_issue" if active_issue_id else "select_backlog_item",
                "issue_id": active_issue_id,
                "allowed": not dirty and qa_ok and validation_ok,
                "reason": recommended_action,
            }
        ],
    }
