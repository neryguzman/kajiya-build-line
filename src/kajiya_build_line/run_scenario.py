from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_input_file(root: Path, item: dict[str, Any]) -> str:
    rel_path = item["path"]
    target = root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if "content_json" in item:
        target.write_text(json.dumps(item["content_json"], indent=2, ensure_ascii=False) + "\n")
    else:
        target.write_text(str(item.get("content", "")))

    return rel_path


def run_shell_command(command: str, cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    parsed_json: Any = None
    if stdout:
        try:
            parsed_json = json.loads(stdout)
        except json.JSONDecodeError:
            parsed_json = None

    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": result.returncode,
        "ok": result.returncode == 0,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_json": parsed_json,
    }


def evaluate_simple_json_path(data: Any, path: str) -> Any:
    if path == "$":
        return data

    if not path.startswith("$."):
        raise ValueError(f"Unsupported JSON path: {path}")

    current = data
    parts = path[2:].split(".")

    for part in parts:
        if part == "length":
            if isinstance(current, list):
                current = len(current)
            else:
                raise ValueError(f"Cannot evaluate length on non-list for path: {path}")
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            raise ValueError(f"Cannot access {part} on non-object for path: {path}")

    return current


def choose_assertion_source(
    source: str | None,
    command_results: list[dict[str, Any]],
) -> Any:
    if not command_results:
        return None

    aliases = {
        "first_add_issue_result": 0,
        "current_project": 1,
        "backlog": 2,
        "duplicate_add_issue_result": 3,
    }

    if source in aliases and aliases[source] < len(command_results):
        return command_results[aliases[source]].get("stdout_json")

    if source and source.startswith("command_"):
        try:
            index = int(source.removeprefix("command_"))
        except ValueError:
            return None
        if 0 <= index < len(command_results):
            return command_results[index].get("stdout_json")

    return command_results[-1].get("stdout_json")


def evaluate_assertion(assertion: dict[str, Any], command_results: list[dict[str, Any]]) -> dict[str, Any]:
    source = assertion.get("source")
    json_path = assertion.get("json_path")
    data = choose_assertion_source(source, command_results)

    actual = None
    error = None
    if json_path:
        try:
            actual = evaluate_simple_json_path(data, json_path)
        except Exception as exc:  # noqa: BLE001 - deterministic error packet
            error = str(exc)

    ok = error is None
    if "equals" in assertion:
        ok = ok and actual == assertion["equals"]
    if "contains" in assertion:
        ok = ok and assertion["contains"] in str(actual)

    return {
        "description": assertion.get("description"),
        "source": source,
        "json_path": json_path,
        "expected_equals": assertion.get("equals"),
        "expected_contains": assertion.get("contains"),
        "actual": actual,
        "ok": ok,
        "error": error,
    }


def run_scenario(root: Path, scenario_path: Path) -> dict[str, Any]:
    root = root.resolve()
    scenario_path = (root / scenario_path).resolve() if not scenario_path.is_absolute() else scenario_path

    if not scenario_path.exists():
        return {
            "schema_version": "kajiya.run_scenario_result.v1",
            "kind": "kajiya_run_scenario_result",
            "ok": False,
            "pi_dev_id": "kajiya_run_scenario",
            "runtime_status": "scenario_file_missing",
            "scenario_path": str(scenario_path),
            "next_safe_actions": [],
        }

    try:
        scenario = load_json(scenario_path)
    except json.JSONDecodeError as exc:
        return {
            "schema_version": "kajiya.run_scenario_result.v1",
            "kind": "kajiya_run_scenario_result",
            "ok": False,
            "pi_dev_id": "kajiya_run_scenario",
            "runtime_status": "invalid_scenario_json",
            "scenario_path": str(scenario_path),
            "error": str(exc),
            "next_safe_actions": [],
        }

    with tempfile.TemporaryDirectory(prefix="kajiya-scenario-") as tmp:
        workspace = Path(tmp)

        written_inputs = [
            write_input_file(workspace, item)
            for item in scenario.get("input_files", [])
        ]

        command_results: list[dict[str, Any]] = []

        for command in scenario.get("setup_commands", []):
            command_results.append(run_shell_command(command, workspace))

        for command in scenario.get("commands", []):
            command_results.append(run_shell_command(command, workspace))

        # Assertions are intended to evaluate the main scenario commands, not setup.
        setup_count = len(scenario.get("setup_commands", []))
        main_command_results = command_results[setup_count:]

        assertion_results = [
            evaluate_assertion(assertion, main_command_results)
            for assertion in scenario.get("assertions", [])
        ]

        # Setup commands must succeed because they prepare the scenario workspace.
        # Main scenario commands may intentionally return non-zero when testing
        # controlled negative behavior, such as duplicate_issue_id.
        setup_results = command_results[:setup_count]
        setup_ok = all(result["ok"] for result in setup_results)
        assertions_ok = all(result["ok"] for result in assertion_results)
        ok = setup_ok and assertions_ok

        return {
            "schema_version": "kajiya.run_scenario_result.v1",
            "kind": "kajiya_run_scenario_result",
            "ok": ok,
            "pi_dev_id": "kajiya_run_scenario",
            "runtime_status": "scenario_passed" if ok else "scenario_failed",
            "project_root": str(root),
            "scenario_path": str(scenario_path.relative_to(root)),
            "scenario_id": scenario.get("scenario_id"),
            "issue_id": scenario.get("issue_id"),
            "workspace_policy": "temporary_directory_auto_cleanup",
            "written_inputs": written_inputs,
            "command_results": command_results,
            "assertion_results": assertion_results,
            "next_safe_actions": [
                {
                    "action": "continue" if ok else "review_failure_packet",
                    "allowed": True,
                }
            ],
        }
