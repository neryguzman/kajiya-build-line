from __future__ import annotations

from pathlib import Path
from typing import Any

from kajiya_build_line.project_detect import run_command


def build_qa_payload(start: Path | None = None) -> dict[str, Any]:
    root = (start or Path.cwd()).resolve()

    checks = [
        {
            "name": "git_diff_check",
            "command": ["git", "--no-pager", "diff", "--check"],
        },
        {
            "name": "python_compileall_src",
            "command": ["python", "-m", "compileall", "src"],
        },
    ]

    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for check in checks:
        result = run_command(check["command"], root)
        entry = {
            "name": check["name"],
            **result,
        }
        results.append(entry)
        if not result["ok"]:
            failures.append(entry)

    ok = not failures

    return {
        "schema_version": "kajiya.qa.v1",
        "kind": "kajiya_qa",
        "ok": ok,
        "pi_dev_id": "kajiya_qa",
        "runtime_status": "qa_passed" if ok else "qa_failed",
        "project_root": str(root),
        "checks": results,
        "failures": failures,
        "next_safe_actions": [
            {
                "action": "commit_or_continue",
                "reason": "QA passed." if ok else "Fix failing checks before proceeding.",
                "allowed": ok,
            }
        ],
    }
