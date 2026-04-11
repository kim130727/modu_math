from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import load_contract_json
from .schema import SchemaValidationError, validate_layout_diff_json, validate_layout_json, validate_semantic_json


class BundleValidationError(SchemaValidationError):
    pass


def load_schema(name: str) -> dict[str, Any]:
    return load_contract_json(name)


def validate_json(data: dict[str, Any], schema: dict[str, Any]) -> None:
    schema_id = schema.get("$id", "")
    if "semantic" in schema_id:
        validate_semantic_json(data)
        return
    if "layout_diff" in schema_id:
        validate_layout_diff_json(data)
        return
    if "layout" in schema_id:
        validate_layout_json(data)
        return
    raise BundleValidationError(f"Unsupported schema id for validation: {schema_id}")


def validate_semantic(data: dict[str, Any]) -> None:
    validate_semantic_json(data)


def validate_layout(data: dict[str, Any]) -> None:
    validate_layout_json(data)


def validate_layout_diff(data: dict[str, Any]) -> None:
    validate_layout_diff_json(data)


def validate_order(data: dict[str, Any], profile: dict[str, Any], kind: str) -> None:
    if kind == "semantic":
        expected = profile["semantic_root_order"]
    elif kind == "layout":
        expected = profile["layout_root_order"]
    elif kind == "layout_diff":
        expected = profile["layout_diff_root_order"]
    else:
        raise BundleValidationError(f"Unsupported order kind: {kind}")

    present_expected = [k for k in expected if k in data]
    actual_prefix = list(data.keys())[: len(present_expected)]
    if actual_prefix != present_expected:
        raise BundleValidationError(
            f"Root key order mismatch for {kind}: expected prefix {present_expected}, got {actual_prefix}"
        )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_problem_bundle(path: str | Path) -> list[str]:
    base = Path(path)
    errors: list[str] = []
    profile = load_contract_json("canonical_order_profile.json")

    semantic_path = base / "json" / "semantic_final" / "semantic_final.json"
    layout_path = base / "json" / "layout_final" / "layout_final.json"
    layout_diff_path = base / "json" / "layout_final" / "layout_diff.json"

    if not semantic_path.exists():
        errors.append(f"Missing semantic file: {semantic_path}")
    else:
        try:
            semantic = _read_json(semantic_path)
            validate_semantic(semantic)
            validate_order(semantic, profile, "semantic")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Semantic validation failed ({semantic_path}): {exc}")

    if not layout_path.exists():
        errors.append(f"Missing layout file: {layout_path}")
    else:
        try:
            layout = _read_json(layout_path)
            validate_layout(layout)
            validate_order(layout, profile, "layout")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Layout validation failed ({layout_path}): {exc}")

    if layout_diff_path.exists():
        try:
            layout_diff = _read_json(layout_diff_path)
            validate_layout_diff(layout_diff)
            validate_order(layout_diff, profile, "layout_diff")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Layout diff validation failed ({layout_diff_path}): {exc}")

    return errors


def validate_all_examples(root: str | Path = "examples/problem") -> dict[str, list[str]]:
    root_path = Path(root)
    failures: dict[str, list[str]] = {}
    if not root_path.exists():
        return failures

    for problem_dir in sorted([d for d in root_path.iterdir() if d.is_dir()], key=lambda p: p.name):
        errors = validate_problem_bundle(problem_dir)
        if errors:
            failures[str(problem_dir)] = errors
    return failures
