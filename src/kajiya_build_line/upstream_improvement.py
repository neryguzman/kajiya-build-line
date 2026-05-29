from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "upstream-improvement"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def create_upstream_improvement(
    root: Path,
    title: str,
    source_project: str,
    problem: str,
    recommendation: str,
    evidence: list[str],
    target_files: list[str],
    validation_commands: list[str],
) -> dict[str, Any]:
    root = root.resolve()
    today = date.today().isoformat()
    slug = slugify(title)
    rel_path = f"docs/upstream-improvements/{slug}.json"
    full_path = root / rel_path

    if full_path.exists():
        return {
            "schema_version": "kajiya.upstream_improvement_result.v1",
            "kind": "kajiya_upstream_improvement_result",
            "ok": False,
            "pi_dev_id": "kajiya_upstream_improvement",
            "runtime_status": "blocked_existing_proposal",
            "proposal_path": rel_path,
            "next_safe_actions": [
                {
                    "action": "review_existing_proposal",
                    "path": rel_path,
                }
            ],
        }

    proposal = {
        "schema_version": "kajiya.upstream_improvement.v1",
        "kind": "kajiya_upstream_improvement",
        "created_at": today,
        "updated_at": today,
        "title": title,
        "slug": slug,
        "source_project": source_project,
        "target_project": "kajiya-build-line",
        "problem": problem,
        "recommendation": recommendation,
        "evidence": evidence,
        "target_files": target_files,
        "validation_commands": validation_commands,
        "status": "proposed",
        "next_steps": [
            "Review proposal in the source repository.",
            "Create or link a backlog item in the main kajiya-build-line repository.",
            "Use the proposal as task-brief input for upstream implementation.",
            "Run QA and JSON Schema validation in the main kajiya-build-line repository.",
            "Merge/push upstream changes.",
            "Update child repositories to the improved Build Line behavior.",
        ],
    }

    write_json(full_path, proposal)

    return {
        "schema_version": "kajiya.upstream_improvement_result.v1",
        "kind": "kajiya_upstream_improvement_result",
        "ok": True,
        "pi_dev_id": "kajiya_upstream_improvement",
        "runtime_status": "upstream_improvement_created",
        "proposal_path": rel_path,
        "title": title,
        "source_project": source_project,
        "target_project": "kajiya-build-line",
        "updated_files": [rel_path],
        "next_safe_actions": [
            {
                "action": "review_proposal",
                "path": rel_path,
            },
            {
                "action": "propose_upstream",
                "target_project": "kajiya-build-line",
                "reason": "Reusable framework improvements belong upstream.",
            },
        ],
    }
