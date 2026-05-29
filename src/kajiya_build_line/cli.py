from __future__ import annotations

import json
import sys
from pathlib import Path

from kajiya_build_line.project_detect import build_status_payload
from kajiya_build_line.qa import build_qa_payload


def print_json(payload: dict) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("ok") else 1


def status() -> int:
    return print_json(build_status_payload(Path.cwd()))


def qa() -> int:
    return print_json(build_qa_payload(Path.cwd()))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"help", "--help", "-h"}:
        print("Usage: kajiya-build-line status|qa")
        return 0

    command = argv[0]

    if command == "status":
        return status()

    if command == "qa":
        return qa()

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Usage: kajiya-build-line status|qa", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
