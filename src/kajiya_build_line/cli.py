from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def status() -> int:
    cwd = Path.cwd()
    root = find_project_root(cwd)

    files = {
        "kajiya_project": root / ".kajiya" / "project.json",
        "backlog": root / "docs" / "state" / "backlog.json",
        "current_project": root / "docs" / "state" / "current-project.json",
        "handoff_protocol": root / "docs" / "LLM_HANDOFF_PROTOCOL.md",
        "pi_dev_registry": root / "docs" / "state" / "pi-dev-registry.json",
    }

    git_branch = run_git(["branch", "--show-current"], root)
    git_status = run_git(["status", "--short"], root)
    latest_commit = run_git(["--no-pager", "log", "--oneline", "-1"], root)

    payload = {
        "ok": True,
        "tool": "kajiya-build-line",
        "command": "status",
        "cwd": str(cwd),
        "project_root": str(root),
        "git": {
            "branch": git_branch,
            "latest_commit": latest_commit,
            "dirty": bool(git_status),
            "status_short": git_status.splitlines() if git_status else [],
        },
        "project_files": {
            name: {
                "path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
                "exists": path.exists(),
            }
            for name, path in files.items()
        },
        "next_safe_actions": [
            {
                "action": "init_project_profile",
                "available": not files["kajiya_project"].exists(),
                "command": "kajiya-build-line init",
            },
            {
                "action": "read_backlog",
                "available": files["backlog"].exists(),
                "path": "docs/state/backlog.json",
            },
            {
                "action": "read_handoff",
                "available": files["handoff_protocol"].exists(),
                "path": "docs/LLM_HANDOFF_PROTOCOL.md",
            },
        ],
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"help", "--help", "-h"}:
        print("Usage: kajiya-build-line status")
        return 0

    command = argv[0]

    if command == "status":
        return status()

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Usage: kajiya-build-line status", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
