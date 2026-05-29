from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def validate_pair(root: Path, instance_path: str, schema_path: str) -> dict[str, Any]:
    instance_full = root / instance_path
    schema_full = root / schema_path

    result: dict[str, Any] = {
        "instance_path": instance_path,
        "schema_path": schema_path,
        "ok": False,
        "errors": [],
    }

    if not instance_full.exists():
        result["runtime_status"] = "missing_instance"
        result["errors"].append(f"Missing instance: {instance_path}")
        return result

    if not schema_full.exists():
        result["runtime_status"] = "missing_schema"
        result["errors"].append(f"Missing schema: {schema_path}")
        return result

    try:
        instance = load_json(instance_full)
        schema = load_json(schema_full)
    except Exception as exc:
        result["runtime_status"] = "invalid_json"
        result["errors"].append(str(exc))
        return result

    try:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            result["runtime_status"] = "schema_validation_failed"
            result["errors"] = [
                {
                    "path": list(error.path),
                    "message": error.message,
                    "validator": error.validator,
                }
                for error in errors
            ]
            return result

        result["ok"] = True
        result["runtime_status"] = "schema_validation_passed"
        return result
    except Exception as exc:
        result["runtime_status"] = "validator_error"
        result["errors"].append(str(exc))
        return result


def build_validation_payload(root: Path) -> dict[str, Any]:
    root = root.resolve()

    validation_pairs = [
        {
            "instance_path": ".kajiya/project.json",
            "schema_path": "docs/schemas/kajiya-project.schema.json",
        },
        {
            "instance_path": "docs/task-briefs/KBL-008.json",
            "schema_path": "docs/schemas/kajiya-task-brief.schema.json",
        },
    ]

    upstream_dir = root / "docs" / "upstream-improvements"
    if upstream_dir.exists():
        for path in sorted(upstream_dir.glob("*.json")):
            validation_pairs.append(
                {
                    "instance_path": str(path.relative_to(root)),
                    "schema_path": "docs/schemas/kajiya-upstream-improvement.schema.json",
                }
            )

    test_scenario_dir = root / "docs" / "test-scenarios"
    if test_scenario_dir.exists():
        for path in sorted(test_scenario_dir.glob("*.json")):
            validation_pairs.append(
                {
                    "instance_path": str(path.relative_to(root)),
                    "schema_path": "docs/schemas/kajiya-test-scenario.schema.json",
                }
            )

    results = [
        validate_pair(root, pair["instance_path"], pair["schema_path"])
        for pair in validation_pairs
    ]

    ok = all(item.get("ok") for item in results)

    return {
        "schema_version": "kajiya.validation.v1",
        "kind": "kajiya_validation",
        "ok": ok,
        "pi_dev_id": "kajiya_validate_json",
        "runtime_status": "json_validation_passed" if ok else "json_validation_failed",
        "project_root": str(root),
        "validated": results,
        "next_safe_actions": [
            {
                "action": "continue",
                "reason": "JSON validation passed." if ok else "Fix JSON validation errors before proceeding.",
                "allowed": ok,
            }
        ],
    }
