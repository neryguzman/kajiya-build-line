from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from kajiya_build_line.backlog import close_issue
from kajiya_build_line.evidence import build_evidence_payload
from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.summary import build_summary_payload
from kajiya_build_line.task_brief import create_task_brief
from kajiya_build_line.validate_json import build_validation_payload


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def handle_summary(args: argparse.Namespace) -> int:
    return print_json(build_summary_payload(Path.cwd()))


def handle_status(args: argparse.Namespace) -> int:
    return print_json(build_status_payload(Path.cwd()))


def handle_qa(args: argparse.Namespace) -> int:
    return print_json(build_qa_payload(Path.cwd()))


def handle_validate_json(args: argparse.Namespace) -> int:
    return print_json(build_validation_payload(Path.cwd()))


def handle_evidence(args: argparse.Namespace) -> int:
    payload = build_evidence_payload(
        root=Path.cwd(),
        read_paths=args.read,
        list_paths=args.list,
        grep_patterns=args.grep,
        grep_search_path=args.grep_path,
        git_log_limit=args.git_log,
    )
    return print_json(payload)


def handle_task_brief(args: argparse.Namespace) -> int:
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


def handle_close_issue(args: argparse.Namespace) -> int:
    payload = close_issue(
        root=Path.cwd(),
        issue_id=args.issue_id,
        next_issue_id=args.next_issue_id,
        evidence=args.evidence,
        completion_note=args.completion_note,
        commit=args.commit,
    )
    return print_json(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kajiya-build-line",
        description="Kajiya Build Line deterministic CLI.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser("summary", help="Show compact operator status summary.")
    summary_parser.set_defaults(handler=handle_summary)

    status_parser = subparsers.add_parser("status", help="Inspect project state.")
    status_parser.set_defaults(handler=handle_status)

    qa_parser = subparsers.add_parser("qa", help="Run deterministic QA checks.")
    qa_parser.set_defaults(handler=handle_qa)

    validate_parser = subparsers.add_parser(
        "validate-json",
        help="Validate durable JSON artifacts against JSON Schemas.",
    )
    validate_parser.set_defaults(handler=handle_validate_json)

    evidence_parser = subparsers.add_parser(
        "evidence",
        help="Collect read-only project evidence.",
    )
    evidence_parser.add_argument("--read", action="append", default=[])
    evidence_parser.add_argument("--list", action="append", default=[])
    evidence_parser.add_argument("--grep", action="append", default=[])
    evidence_parser.add_argument("--grep-path", default=".")
    evidence_parser.add_argument("--git-log", type=int)
    evidence_parser.set_defaults(handler=handle_evidence)

    task_brief_parser = subparsers.add_parser(
        "task-brief",
        help="Create a human-authored Builder task brief.",
    )
    task_brief_parser.add_argument("--issue-id", required=True)
    task_brief_parser.add_argument("--instruction", required=True)
    task_brief_parser.add_argument("--evidence", action="append", default=[])
    task_brief_parser.add_argument("--allowed-file", action="append", default=[])
    task_brief_parser.add_argument("--validation", action="append", default=[])
    task_brief_parser.add_argument("--forbidden-action", action="append", default=[])
    task_brief_parser.set_defaults(handler=handle_task_brief)

    close_issue_parser = subparsers.add_parser(
        "close-issue",
        help="Close one backlog issue and optionally activate the next issue.",
    )
    close_issue_parser.add_argument("--issue-id", required=True)
    close_issue_parser.add_argument("--next-issue-id")
    close_issue_parser.add_argument("--evidence", action="append", default=[])
    close_issue_parser.add_argument("--completion-note", required=True)
    close_issue_parser.add_argument("--commit")
    close_issue_parser.set_defaults(handler=handle_close_issue)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()

    if not argv:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
