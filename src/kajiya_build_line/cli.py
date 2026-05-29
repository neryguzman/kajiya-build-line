from __future__ import annotations

import json
import sys
from pathlib import Path

from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.backlog import close_issue


def print_json(payload: dict) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def status() -> int:
    return print_json(build_status_payload(Path.cwd()))


def qa() -> int:
    return print_json(build_qa_payload(Path.cwd()))


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
        print("Usage: kajiya-build-line status|qa|close-issue")
        return 0

    command = argv[0]

    if command == "status":
        return status()

    if command == "qa":
        return qa()

    if command == "close-issue":
        return close_issue_command(argv[1:])

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Usage: kajiya-build-line status|qa|close-issue", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
