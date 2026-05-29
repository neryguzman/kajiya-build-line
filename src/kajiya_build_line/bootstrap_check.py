from __future__ import annotations

from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    ".kajiya/project.json",
    "docs/state/backlog.json",
    "docs/state/current-project.json",
    "docs/LLM_HANDOFF_PROTOCOL.md",
]

REQUIRED_DIRS = [
    "docs/evidence",
    "docs/task-briefs",
]


def build_bootstrap_check_payload(start: Path | None = None) -> dict[str, Any]:
    root = (start or Path.cwd()).resolve()

    required = [*REQUIRED_FILES, *REQUIRED_DIRS]

    present = []
    missing = []

    for rel in REQUIRED_FILES:
        if (root / rel).is_file():
            present.append(rel)
        else:
            missing.append(rel)

    for rel in REQUIRED_DIRS:
        if (root / rel).is_dir():
            present.append(rel)
        else:
            missing.append(rel)

    initialized = not missing

    if initialized:
        recommended_action = "Repository is initialized. Use kajiya-build-line next."
        next_action = {
            "action": "continue_normal_flow",
            "command": "kajiya-build-line next",
            "allowed": True,
        }
    else:
        recommended_action = "Repository is missing Kajiya Build Line files. Run kajiya-build-line init-project with project metadata."
        next_action = {
            "action": "run_init_project",
            "command": "kajiya-build-line init-project --project-id <id> --project-name <name> --project-type <type>",
            "allowed": True,
        }

    return {
        "schema_version": "kajiya.bootstrap_check.v1",
        "kind": "kajiya_bootstrap_check",
        "ok": True,
        "pi_dev_id": "kajiya_bootstrap_check",
        "runtime_status": "initialized" if initialized else "missing_required_files",
        "project_root": str(root),
        "initialized": initialized,
        "present": present,
        "missing": missing,
        "required_files": required,
        "recommended_action": recommended_action,
        "next_safe_actions": [next_action],
    }
