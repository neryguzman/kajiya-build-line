from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from kajiya_build_line.add_issue import add_issue
from kajiya_build_line.backlog import close_issue
from kajiya_build_line.backlog_orient import build_backlog_orientation_payload
from kajiya_build_line.bootstrap_check import build_bootstrap_check_payload
from kajiya_build_line.checkpoint import build_checkpoint_payload
from kajiya_build_line.evidence import build_evidence_payload
from kajiya_build_line.init_project import init_project
from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload
from kajiya_build_line.summary import build_summary_payload
from kajiya_build_line.next_action import build_next_payload
from kajiya_build_line.run_scenario import run_scenario
from kajiya_build_line.task_brief import create_task_brief
from kajiya_build_line.upstream_improvement import create_upstream_improvement
from kajiya_build_line.validate_json import build_validation_payload


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def handle_add_issue(args: argparse.Namespace) -> int:
    return print_json(
        add_issue(
            root=Path.cwd(),
            issue_id=args.issue_id,
            title=args.title,
            priority=args.priority,
            issue_type=args.type,
            problem=args.problem,
            expected_behavior=args.expected_behavior,
            proposed_changes=args.proposed_change,
            files_likely_to_change=args.file,
            validation_commands=args.validation,
            close_criteria=args.close_criterion,
            activate=args.activate,
            from_json_file=args.from_json,
        )
    )


def handle_backlog(args: argparse.Namespace) -> int:
    return print_json(build_backlog_orientation_payload(Path.cwd()))


def handle_bootstrap_check(args: argparse.Namespace) -> int:
    return print_json(build_bootstrap_check_payload(Path.cwd()))


def handle_init_project(args: argparse.Namespace) -> int:
    return print_json(
        init_project(
            root=Path.cwd(),
            project_id=args.project_id,
            project_name=args.project_name,
            project_type=args.project_type,
        )
    )


def handle_next(args: argparse.Namespace) -> int:
    return print_json(build_next_payload(Path.cwd()))


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


def handle_upstream_improvement(args: argparse.Namespace) -> int:
    return print_json(
        create_upstream_improvement(
            root=Path.cwd(),
            title=args.title,
            source_project=args.source_project,
            problem=args.problem,
            recommendation=args.recommendation,
            evidence=args.evidence,
            target_files=args.target_file,
            validation_commands=args.validation,
        )
    )


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


def handle_checkpoint(args: argparse.Namespace) -> int:
    return print_json(build_checkpoint_payload(Path.cwd()))


def handle_run_scenario(args: argparse.Namespace) -> int:
    return print_json(run_scenario(root=Path.cwd(), scenario_path=args.scenario))


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

    add_issue_parser = subparsers.add_parser(
        "add-issue",
        help="Add a backlog issue deterministically.",
    )
    add_issue_parser.add_argument("--issue-id")
    add_issue_parser.add_argument("--title")
    add_issue_parser.add_argument("--priority")
    add_issue_parser.add_argument("--type")
    add_issue_parser.add_argument("--problem")
    add_issue_parser.add_argument("--expected-behavior")
    add_issue_parser.add_argument("--proposed-change", action="append", default=[])
    add_issue_parser.add_argument("--file", action="append", default=[])
    add_issue_parser.add_argument("--validation", action="append", default=[])
    add_issue_parser.add_argument("--close-criterion", action="append", default=[])
    add_issue_parser.add_argument("--activate", action="store_true")
    add_issue_parser.add_argument("--from-json", type=Path, help="Load issue fields from a JSON file")
    add_issue_parser.set_defaults(handler=handle_add_issue)

    backlog_parser = subparsers.add_parser("backlog", help="Show deterministic backlog orientation.")
    backlog_parser.set_defaults(handler=handle_backlog)

    bootstrap_check_parser = subparsers.add_parser("bootstrap-check", help="Check whether the current repo has Kajiya Build Line files.")
    bootstrap_check_parser.set_defaults(handler=handle_bootstrap_check)

    init_project_parser = subparsers.add_parser("init-project", help="Bootstrap Kajiya Build Line files into the current repo.")
    init_project_parser.add_argument("--project-id", required=True)
    init_project_parser.add_argument("--project-name", required=True)
    init_project_parser.add_argument("--project-type", required=True)
    init_project_parser.set_defaults(handler=handle_init_project)

    next_parser = subparsers.add_parser("next", help="Show the next recommended operator action.")
    next_parser.set_defaults(handler=handle_next)

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

    upstream_parser = subparsers.add_parser(
        "upstream-improvement",
        help="Create an upstream improvement proposal artifact.",
    )
    upstream_parser.add_argument("--title", required=True)
    upstream_parser.add_argument("--source-project", required=True)
    upstream_parser.add_argument("--problem", required=True)
    upstream_parser.add_argument("--recommendation", required=True)
    upstream_parser.add_argument("--evidence", action="append", default=[])
    upstream_parser.add_argument("--target-file", action="append", default=[])
    upstream_parser.add_argument("--validation", action="append", default=[])
    upstream_parser.set_defaults(handler=handle_upstream_improvement)

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

    checkpoint_parser = subparsers.add_parser(
        "checkpoint",
        help="Show read-only deterministic checkpoint orientation.",
    )
    checkpoint_parser.set_defaults(handler=handle_checkpoint)

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

    run_scenario_parser = subparsers.add_parser(
        "run-scenario", help="Execute a test scenario from a JSON file."
    )
    run_scenario_parser.add_argument(
        "--scenario", type=Path, required=True, help="Path to the scenario JSON file"
    )
    run_scenario_parser.set_defaults(handler=handle_run_scenario)

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
