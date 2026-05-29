from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def run_command(args: list[str], cwd: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd),
            check=False,
            text=True,
            capture_output=True,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "command": " ".join(args),
        }
    except Exception as exc:
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
            "command": " ".join(args),
        }


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def read_json_file(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        return {
            "_read_error": str(exc),
            "_path": str(path),
        }


def read_text_file(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return path.read_text()
    except Exception as exc:
        return f"READ_ERROR: {exc}"


def project_paths(root: Path) -> dict[str, Path]:
    return {
        "project_profile": root / ".kajiya" / "project.json",
        "current_project": root / "docs" / "state" / "current-project.json",
        "backlog": root / "docs" / "state" / "backlog.json",
        "handoff_protocol": root / "docs" / "LLM_HANDOFF_PROTOCOL.md",
    }


def summarize_backlog(backlog: dict[str, Any] | None) -> dict[str, Any] | None:
    if not backlog:
        return None

    items = backlog.get("items", [])
    counts: dict[str, int] = {}
    active_candidates = []

    for item in items:
        status = item.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
        if status != "done":
            active_candidates.append({
                "issue_id": item.get("issue_id"),
                "title": item.get("title"),
                "status": status,
                "priority": item.get("priority"),
                "type": item.get("type"),
            })

    return {
        "source_of_truth": backlog.get("source_of_truth"),
        "project_id": backlog.get("project_id"),
        "updated_at": backlog.get("updated_at"),
        "counts_by_status": counts,
        "active_candidates": active_candidates,
    }


def build_status_payload(start: Path | None = None) -> dict[str, Any]:
    cwd = start or Path.cwd()
    root = find_project_root(cwd)
    paths = project_paths(root)

    project_profile = read_json_file(paths["project_profile"])
    current_project = read_json_file(paths["current_project"])
    backlog = read_json_file(paths["backlog"])
    handoff = read_text_file(paths["handoff_protocol"])

    missing = [
        str(path.relative_to(root))
        for path in paths.values()
        if not path.exists()
    ]

    git_status = run_command(["git", "status", "--short"], root)
    git_log = run_command(["git", "--no-pager", "log", "--oneline", "-12"], root)

    dirty = bool(git_status.get("stdout"))

    if missing:
        runtime_status = "missing_required_evidence"
    elif dirty:
        runtime_status = "dirty_worktree"
    else:
        runtime_status = "ready_for_backlog_selection"

    next_safe_actions = []
    if ".kajiya/project.json" in missing:
        next_safe_actions.append({
            "action": "initialize_project_profile",
            "issue_id": "KBL-003",
            "requires_human_approval": True,
        })

    backlog_summary = summarize_backlog(backlog)
    if backlog_summary and backlog_summary.get("active_candidates"):
        next_safe_actions.append({
            "action": "select_backlog_item",
            "candidates": backlog_summary["active_candidates"],
            "requires_human_approval": True,
        })

    if not next_safe_actions:
        next_safe_actions.append({
            "action": "stop",
            "reason": "No obvious next action found.",
        })

    return {
        "schema_version": "kajiya.status.v1",
        "kind": "kajiya_status",
        "ok": not missing,
        "pi_dev_id": "kajiya_status",
        "runtime_status": runtime_status,
        "project_root": str(root),
        "cwd": str(cwd.resolve()),
        "project_profile": project_profile,
        "current_project": current_project,
        "backlog_summary": backlog_summary,
        "handoff_present": handoff is not None,
        "git": {
            "status_short": git_status,
            "log_oneline_12": git_log,
            "dirty": dirty,
        },
        "missing_evidence": missing,
        "next_safe_actions": next_safe_actions,
    }
