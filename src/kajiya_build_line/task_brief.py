from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def safe_issue_id(value: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
    cleaned = "".join(ch for ch in value if ch in allowed)
    if not cleaned:
        raise ValueError("issue_id is required")
    return cleaned


def create_task_brief(
    root: Path,
    issue_id: str,
    instruction: str,
    evidence: list[str],
    allowed_files: list[str],
    validation_commands: list[str],
    forbidden_actions: list[str],
) -> dict[str, Any]:
    root = root.resolve()
    issue_id = safe_issue_id(issue_id)

    if not instruction.strip():
        return {
            "schema_version": "kajiya.task_brief_result.v1",
            "kind": "kajiya_task_brief_result",
            "ok": False,
            "pi_dev_id": "kajiya_task_brief",
            "runtime_status": "missing_instruction",
            "next_safe_actions": [
                {
                    "action": "stop",
                    "reason": "A human-authored instruction is required.",
                }
            ],
        }

    brief_dir = root / "docs" / "task-briefs"
    brief_dir.mkdir(parents=True, exist_ok=True)
    brief_path = brief_dir / f"{issue_id}.json"

    today = date.today().isoformat()

    brief = {
        "schema_version": "kajiya.task_brief.v1",
        "kind": "kajiya_task_brief",
        "issue_id": issue_id,
        "created_at": today,
        "updated_at": today,
        "source_of_truth": str(brief_path.relative_to(root)),
        "human_instruction": instruction.strip(),
        "evidence_refs": evidence,
        "allowed_files": allowed_files,
        "validation_commands": validation_commands,
        "forbidden_actions": forbidden_actions or [
            "Do not modify files outside allowed_files.",
            "Do not invoke external writes.",
            "Do not commit.",
            "Do not close issues.",
            "Do not use direct Gemini SDK.",
        ],
        "builder_mode": "bounded_patch_plan",
        "requires_human_approval": True,
        "next_safe_actions": [
            {
                "action": "run_builder_plan",
                "command": f"/kajiya-builder-plan issue_id={issue_id}",
                "brief": str(brief_path.relative_to(root)),
            },
            {
                "action": "review_brief",
                "path": str(brief_path.relative_to(root)),
            },
        ],
    }

    brief_path.write_text(json.dumps(brief, indent=2, ensure_ascii=False) + "\n")

    return {
        "schema_version": "kajiya.task_brief_result.v1",
        "kind": "kajiya_task_brief_result",
        "ok": True,
        "pi_dev_id": "kajiya_task_brief",
        "runtime_status": "task_brief_created",
        "issue_id": issue_id,
        "brief_path": str(brief_path.relative_to(root)),
        "updated_files": [str(brief_path.relative_to(root))],
        "next_safe_actions": brief["next_safe_actions"],
    }
