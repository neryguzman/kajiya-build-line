from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


MAX_READ_CHARS = 20000
MAX_GREP_MATCHES = 200


def safe_rel_path(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    root_resolved = root.resolve()
    if candidate == root_resolved or root_resolved in candidate.parents:
        return candidate
    raise ValueError(f"Path escapes project root: {value}")


def path_label(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_file(root: Path, value: str) -> dict[str, Any]:
    try:
        path = safe_rel_path(root, value)
        if not path.exists():
            return {
                "type": "read",
                "path": value,
                "ok": False,
                "error": "file_not_found",
            }
        if not path.is_file():
            return {
                "type": "read",
                "path": value,
                "ok": False,
                "error": "not_a_file",
            }
        text = path.read_text(errors="replace")
        truncated = len(text) > MAX_READ_CHARS
        return {
            "type": "read",
            "path": path_label(root, path),
            "ok": True,
            "truncated": truncated,
            "content": text[:MAX_READ_CHARS],
        }
    except Exception as exc:
        return {
            "type": "read",
            "path": value,
            "ok": False,
            "error": str(exc),
        }


def list_path(root: Path, value: str) -> dict[str, Any]:
    try:
        path = safe_rel_path(root, value)
        if not path.exists():
            return {
                "type": "list",
                "path": value,
                "ok": False,
                "error": "path_not_found",
            }
        if not path.is_dir():
            return {
                "type": "list",
                "path": value,
                "ok": False,
                "error": "not_a_directory",
            }
        entries = []
        for item in sorted(path.iterdir(), key=lambda p: p.name.lower()):
            entries.append({
                "name": item.name,
                "path": path_label(root, item),
                "kind": "dir" if item.is_dir() else "file",
            })
        return {
            "type": "list",
            "path": path_label(root, path),
            "ok": True,
            "entries": entries,
        }
    except Exception as exc:
        return {
            "type": "list",
            "path": value,
            "ok": False,
            "error": str(exc),
        }


def grep_path(root: Path, pattern: str, search_path: str) -> dict[str, Any]:
    try:
        path = safe_rel_path(root, search_path)
        if not path.exists():
            return {
                "type": "grep",
                "pattern": pattern,
                "path": search_path,
                "ok": False,
                "error": "path_not_found",
            }

        files: list[Path]
        if path.is_file():
            files = [path]
        else:
            ignored_parts = {".git", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache"}
            files = [
                p for p in path.rglob("*")
                if p.is_file() and not any(part in ignored_parts for part in p.parts)
            ]

        matches = []
        for file_path in files:
            try:
                text = file_path.read_text(errors="replace")
            except Exception:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if pattern in line:
                    matches.append({
                        "path": path_label(root, file_path),
                        "line": line_no,
                        "text": line[:500],
                    })
                    if len(matches) >= MAX_GREP_MATCHES:
                        return {
                            "type": "grep",
                            "pattern": pattern,
                            "path": path_label(root, path),
                            "ok": True,
                            "truncated": True,
                            "matches": matches,
                        }

        return {
            "type": "grep",
            "pattern": pattern,
            "path": path_label(root, path),
            "ok": True,
            "truncated": False,
            "matches": matches,
        }
    except Exception as exc:
        return {
            "type": "grep",
            "pattern": pattern,
            "path": search_path,
            "ok": False,
            "error": str(exc),
        }


def git_log(root: Path, limit: int) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "--no-pager", "log", "--oneline", f"-{limit}"],
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
        )
        return {
            "type": "git_log",
            "ok": result.returncode == 0,
            "limit": limit,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except Exception as exc:
        return {
            "type": "git_log",
            "ok": False,
            "limit": limit,
            "error": str(exc),
        }


def build_evidence_payload(
    root: Path,
    read_paths: list[str],
    list_paths: list[str],
    grep_patterns: list[str],
    grep_search_path: str,
    git_log_limit: int | None,
) -> dict[str, Any]:
    root = root.resolve()
    results = []

    for item in read_paths:
        results.append(read_file(root, item))

    for item in list_paths:
        results.append(list_path(root, item))

    for pattern in grep_patterns:
        results.append(grep_path(root, pattern, grep_search_path))

    if git_log_limit:
        results.append(git_log(root, git_log_limit))

    ok = all(result.get("ok") for result in results)

    return {
        "schema_version": "kajiya.evidence.v1",
        "kind": "kajiya_evidence",
        "ok": ok,
        "pi_dev_id": "kajiya_evidence",
        "runtime_status": "evidence_collected" if ok else "evidence_partial_or_failed",
        "project_root": str(root),
        "request": {
            "read": read_paths,
            "list": list_paths,
            "grep": grep_patterns,
            "grep_path": grep_search_path,
            "git_log": git_log_limit,
        },
        "results": results,
        "next_safe_actions": [
            {
                "action": "review_evidence",
                "reason": "Use this JSON as Builder input or human review context.",
            }
        ],
    }
