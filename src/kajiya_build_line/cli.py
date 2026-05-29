from __future__ import annotations

import json
import sys
from pathlib import Path

from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.backlog import close_issue
from kajiya_build_line.evidence import build_evidence_payload
from kajiya_build_line.task_brief import create_task_brief


def print_json(payload: dict) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def status() -> int:
    return print_json(build_status_payload(Path.cwd()))


def qa() -> int:
    return print_json(build_qa_payload(Path.cwd()))


def task_brief_command(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="kajiya-build-line task-brief")
    parser.add_argument("--issue-id", required=True)
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--allowed-file", action="append", default=[])
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--forbidden-action", action="append", default=[])

    args = parser.parse_args(argv)

    payload = create_task_brief(
        root=Path.cwd(),
        issue_id=args.issue_id,
        instruction=args.instruction,
        evidence=args.evidence,
        allowed_files=args.allowed_file,
        validation_commands=args.validation,
        forbidden_actions=args.forbidden_action,
    )
    return print_json(payload)


def evidence_command(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="kajiya-build-line evidence")
    parser.add_argument("--read", action="append", default=[])
    parser.add_argument("--list", action="append", default=[])
    parser.add_argument("--grep", action="append", default=[])
    parser.add_argument("--grep-path", default=".")
    parser.add_argument("--git-log", type=int)

    args = parser.parse_args(argv)

    payload = build_evidence_payload(
        root=Path.cwd(),
        read_paths=args.read,
        list_paths=args.list,
        grep_patterns=args.grep,
        grep_search_path=args.grep_path,
        git_log_limit=args.git_log,
    )
    return print_json(payload)


def close_issue_command(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="kajiya-build-line close-issue")
    parser.add_argument("--issue-id", required=True)
    parser.add_argument("--next-issue-id")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--completion-note", required=True)
    parser.add_argument("--commit")

    args = parser.parse_args(argv)

    payload = close_issue(
        root=Path.cwd(),
        issue_id=args.issue_id,
        next_issue_id=args.next_issue_id,
        evidence=args.evidence,
        completion_note=args.completion_note,
        commit=args.commit,
    )
    return print_json(payload)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"help", "--help", "-h"}:
        print("Usage: kajiya-build-line status|qa|close-issue|evidence|task-brief")
        return 0

    command = argv[0]

    if command == "status":
        return status()

    if command == "qa":
        return qa()

    if command == "task-brief":
        return task_brief_command(argv[1:])

    if command == "evidence":
        return evidence_command(argv[1:])

    if command == "close-issue":
        return close_issue_command(argv[1:])

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Usage: kajiya-build-line status|qa|close-issue|evidence|task-brief", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
