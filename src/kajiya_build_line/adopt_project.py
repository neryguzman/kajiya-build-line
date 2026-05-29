from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def count_files(root: Path, rel_dir: str, patterns: tuple[str, ...]) -> int:
    path = root / rel_dir
    if not path.exists() or not path.is_dir():
        return 0

    count = 0
    for pattern in patterns:
        count += len(list(path.glob(pattern)))
    return count


def read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "--no-pager", "log", "--oneline", "-1"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def classify_repo(present: dict[str, bool]) -> str:
    has_state = present["docs/state/current-project.json"] and present["docs/state/backlog.json"]
    has_handoff = present["docs/LLM_HANDOFF_PROTOCOL.md"]
    has_kajiya_dirs = present["docs/schemas"] or present["docs/scenarios"] or present["docs/org-roam"]
    has_build_line_core = present[".kajiya/project.json"] and has_state

    if has_build_line_core and present["AGENTS.md"]:
        return "already_initialized"

    if has_state and has_handoff and has_kajiya_dirs:
        return "mature_kajiya_repo"

    if has_state or has_handoff or has_kajiya_dirs:
        return "partial_kajiya_repo"

    if present[".git"]:
        return "fresh_repo"

    return "incompatible_repo"


def build_adoption_plan(
    classification: str,
    present: dict[str, bool],
    missing_recommended: list[str],
) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []

    if classification == "mature_kajiya_repo":
        plan.append(
            {
                "action": "do_not_run_init_project",
                "reason": "Mature Kajiya repository files already exist and must not be overwritten.",
            }
        )
        if "AGENTS.md" in missing_recommended:
            plan.append(
                {
                    "action": "create_agents_bridge",
                    "reason": "AGENTS.md is missing; create a compact bridge to existing handoff and Build Line rules.",
                    "requires_human_approval": True,
                }
            )
        plan.append(
            {
                "action": "read_existing_handoff",
                "path": "docs/LLM_HANDOFF_PROTOCOL.md",
                "reason": "Existing repo-specific handoff doctrine is authoritative context.",
            }
        )
        plan.append(
            {
                "action": "map_existing_scenarios",
                "paths": ["docs/scenarios", "docs/test-scenarios"],
                "reason": "Existing scenario conventions should be mapped before adding portable Build Line scenarios.",
            }
        )
    elif classification == "fresh_repo":
        plan.append(
            {
                "action": "consider_init_project",
                "command": "kajiya-build-line init-project --project-id PROJECT_ID --project-name PROJECT_NAME --project-type PROJECT_TYPE",
                "requires_human_approval": True,
            }
        )
    elif classification == "already_initialized":
        plan.append(
            {
                "action": "continue_build_line_flow",
                "command": "kajiya-build-line checkpoint",
            }
        )
    else:
        plan.append(
            {
                "action": "manual_review",
                "reason": "Repository has partial or incompatible Kajiya markers. Human/chat should inspect before adopting.",
            }
        )

    if not present["docs/test-scenarios"] and present["docs/scenarios"]:
        plan.append(
            {
                "action": "consider_test_scenario_bridge",
                "reason": "Repo has docs/scenarios but not docs/test-scenarios; map naming before migration.",
                "requires_human_approval": True,
            }
        )

    return plan


def build_adopt_project_payload(root: Path) -> dict[str, Any]:
    root = root.resolve()

    present = {
        ".git": exists(root, ".git"),
        ".kajiya/project.json": exists(root, ".kajiya/project.json"),
        "docs/state/current-project.json": exists(root, "docs/state/current-project.json"),
        "docs/state/backlog.json": exists(root, "docs/state/backlog.json"),
        "docs/LLM_HANDOFF_PROTOCOL.md": exists(root, "docs/LLM_HANDOFF_PROTOCOL.md"),
        "docs/LLM_ENTRYPOINT.md": exists(root, "docs/LLM_ENTRYPOINT.md"),
        "AGENTS.md": exists(root, "AGENTS.md"),
        "docs/org-roam": exists(root, "docs/org-roam"),
        "docs/schemas": exists(root, "docs/schemas"),
        "docs/scenarios": exists(root, "docs/scenarios"),
        "docs/test-scenarios": exists(root, "docs/test-scenarios"),
        ".pi/extensions": exists(root, ".pi/extensions"),
        ".pi/kajiya": exists(root, ".pi/kajiya"),
    }

    counts = {
        "schema_files": count_files(root, "docs/schemas", ("*.json", "*.yaml", "*.yml")),
        "scenario_files": count_files(root, "docs/scenarios", ("*.json", "*.yaml", "*.yml", "*.md")),
        "test_scenario_files": count_files(root, "docs/test-scenarios", ("*.json",)),
        "org_roam_files": count_files(root, "docs/org-roam", ("*.org", "*.md")),
        "pi_extension_files": count_files(root, ".pi/extensions", ("*.ts", "*.js")),
    }

    current_project = read_json_if_exists(root / "docs" / "state" / "current-project.json")
    backlog = read_json_if_exists(root / "docs" / "state" / "backlog.json")

    classification = classify_repo(present)

    recommended_artifacts = [
        "docs/state/current-project.json",
        "docs/state/backlog.json",
        "docs/LLM_HANDOFF_PROTOCOL.md",
        "AGENTS.md",
    ]
    missing_recommended = [
        path for path in recommended_artifacts
        if not present.get(path, False)
    ]

    do_not_run_init_project = classification in {
        "already_initialized",
        "mature_kajiya_repo",
        "partial_kajiya_repo",
    }

    return {
        "schema_version": "kajiya.adopt_project.v1",
        "kind": "kajiya_adopt_project",
        "ok": True,
        "pi_dev_id": "kajiya_adopt_project",
        "runtime_status": classification,
        "project_root": str(root),
        "project_id": (
            current_project.get("project_id")
            if isinstance(current_project, dict)
            else None
        ),
        "active_issue_id": (
            current_project.get("active_issue_id")
            if isinstance(current_project, dict)
            else None
        ),
        "active_workstream": (
            current_project.get("active_workstream")
            if isinstance(current_project, dict)
            else None
        ),
        "backlog_items_count": (
            len(backlog.get("items", []))
            if isinstance(backlog, dict)
            else None
        ),
        "latest_commit": git_head(root),
        "present": present,
        "counts": counts,
        "missing_recommended_artifacts": missing_recommended,
        "do_not_run_init_project": do_not_run_init_project,
        "adoption_plan": build_adoption_plan(
            classification,
            present,
            missing_recommended,
        ),
        "next_safe_actions": [
            {
                "action": "review_adoption_plan",
                "allowed": True,
            },
            {
                "action": "create_agents_bridge",
                "allowed": "AGENTS.md" in missing_recommended,
                "requires_human_approval": True,
            },
        ],
    }
