from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.validate_json import build_validation_payload


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def run_git(root: Path, args: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "command": "git " + " ".join(args),
    }


def build_checkpoint_payload(root: Path) -> dict[str, Any]:
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
            "schema_version": "kajiya.checkpoint.v1",
            "kind": "kajiya_checkpoint",
            "ok": False,
            "pi_dev_id": "kajiya_checkpoint",
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

    current = load_json(current_path)
    backlog = load_json(backlog_path)

    active_issue_id = current.get("active_issue_id")
    active_workstream = current.get("active_workstream")

    status = run_git(root, ["status", "--short"])
    changed_files_result = run_git(root, ["diff", "--name-only"])
    diff_stat_result = run_git(root, ["diff", "--stat"])
    latest_commit_result = run_git(root, ["--no-pager", "log", "--oneline", "-1"])

    status_lines = [line for line in status.get("stdout", "").splitlines() if line.strip()]
    changed_files = [
        line.strip()
        for line in changed_files_result.get("stdout", "").splitlines()
        if line.strip()
    ]

    qa_payload = build_qa_payload(root)
    validation_payload = build_validation_payload(root)

    task_brief_path = None
    if active_issue_id:
        candidate = root / "docs" / "task-briefs" / f"{active_issue_id}.json"
        if candidate.exists():
            task_brief_path = str(candidate.relative_to(root))

    active_item = None
    for item in backlog.get("items", []):
        if item.get("issue_id") == active_issue_id:
            active_item = {
                "issue_id": item.get("issue_id"),
                "title": item.get("title"),
                "status": item.get("status"),
                "priority": item.get("priority"),
                "type": item.get("type"),
            }
            break

    dirty = bool(status_lines)

    if dirty:
        recommended_operator_action = (
            "Review changed files and decide whether to create evidence, update a task brief, "
            "commit manually, or request a bounded Builder action."
        )
    elif active_issue_id:
        recommended_operator_action = current.get("next_recommended_action") or f"Continue {active_issue_id}."
    else:
        recommended_operator_action = "Create or select the next backlog item."

    return {
        "schema_version": "kajiya.checkpoint.v1",
        "kind": "kajiya_checkpoint",
        "ok": True,
        "pi_dev_id": "kajiya_checkpoint",
        "runtime_status": "checkpoint_ready",
        "project_root": str(root),
        "project_id": current.get("project_id") or backlog.get("project_id"),
        "active_issue_id": active_issue_id,
        "active_workstream": active_workstream,
        "active_item": active_item,
        "dirty": dirty,
        "git_status_short": status.get("stdout", ""),
        "changed_files": changed_files,
        "diff_stat": diff_stat_result.get("stdout", ""),
        "latest_commit": latest_commit_result.get("stdout", ""),
        "qa_ok": bool(qa_payload.get("ok")),
        "qa_runtime_status": qa_payload.get("runtime_status"),
        "validation_ok": bool(validation_payload.get("ok")),
        "validation_runtime_status": validation_payload.get("runtime_status"),
        "task_brief_path": task_brief_path,
        "recommended_operator_action": recommended_operator_action,
        "next_human_input_contract": {
            "purpose": "Give the human/chat enough deterministic context to choose the next action without LLM repo rediscovery.",
            "accepted_next_actions": [
                "create_or_update_evidence",
                "create_or_update_task_brief",
                "request_bounded_builder_execution",
                "manual_commit_after_review",
                "close_issue_with_evidence",
                "add_new_backlog_issue",
            ],
            "suggested_fields": {
                "decision": "<one accepted_next_action>",
                "issue_id": active_issue_id,
                "human_reasoning_summary": "<why this action is correct>",
                "allowed_files": changed_files,
                "evidence_paths": [],
                "validation_commands": [
                    "kajiya-build-line qa",
                    "kajiya-build-line validate-json",
                    "git --no-pager diff --check",
                ],
            },
        },
        "safe_commands": [
            "kajiya-build-line checkpoint",
            "kajiya-build-line backlog",
            "kajiya-build-line next",
            "kajiya-build-line qa",
            "kajiya-build-line validate-json",
            "git status --short",
            "git --no-pager diff --stat",
        ],
        "next_safe_actions": [
            {
                "action": "human_review",
                "allowed": True,
                "reason": recommended_operator_action,
            }
        ],
    }
