from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .normalizer import normalize_layout, normalize_layout_diff, normalize_semantic
from .orderer import order_layout, order_layout_diff, order_semantic
from .serializer import serialize_layout, serialize_layout_diff, serialize_semantic
from .validator import validate_layout, validate_layout_diff, validate_semantic


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_canonical_payloads(
    problem_ir,
    *,
    validate: bool = True,
    semantic_options: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    semantic = serialize_semantic(problem_ir, **(semantic_options or {}))
    semantic = normalize_semantic(semantic)
    semantic = order_semantic(semantic)

    layout = serialize_layout(problem_ir)
    layout = normalize_layout(layout)
    layout = order_layout(layout)

    if validate:
        validate_semantic(semantic)
        validate_layout(layout)

    return semantic, layout


def _root_key_diff(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, list[str]]:
    current_keys = set(current.keys())
    baseline_keys = set(baseline.keys())
    return {
        "added": sorted(current_keys - baseline_keys),
        "removed": sorted(baseline_keys - current_keys),
        "changed": sorted([k for k in current_keys & baseline_keys if current.get(k) != baseline.get(k)]),
    }


def _element_key(element: dict[str, Any], index: int) -> str:
    element_id = element.get("id")
    if element_id:
        return f"id:{element_id}"
    return f"index:{index}"


def _element_map(elements: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {_element_key(element, idx): element for idx, element in enumerate(elements)}


def _element_diff(current_elements: list[dict[str, Any]], baseline_elements: list[dict[str, Any]]) -> dict[str, Any]:
    current_map = _element_map(current_elements)
    baseline_map = _element_map(baseline_elements)

    current_keys = set(current_map.keys())
    baseline_keys = set(baseline_map.keys())

    added = sorted(current_keys - baseline_keys)
    removed = sorted(baseline_keys - current_keys)

    modified: list[dict[str, Any]] = []
    for key in sorted(current_keys & baseline_keys):
        current_el = current_map[key]
        baseline_el = baseline_map[key]
        if current_el == baseline_el:
            continue

        changed_fields = sorted(
            [
                field
                for field in set(current_el.keys()) | set(baseline_el.keys())
                if current_el.get(field) != baseline_el.get(field)
            ]
        )
        modified.append({"element_key": key, "changed_fields": changed_fields})

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }


def _build_layout_diff(current: dict[str, Any], baseline: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    root = _root_key_diff(current, baseline)
    current_elements = current.get("elements", []) if isinstance(current.get("elements"), list) else []
    baseline_elements = baseline.get("elements", []) if isinstance(baseline.get("elements"), list) else []
    element = _element_diff(current_elements, baseline_elements)

    diff = {
        "root": root,
        "element": element,
    }
    metrics = {
        "current_total_elements": len(current_elements),
        "baseline_total_elements": len(baseline_elements),
        "element_count_delta": len(current_elements) - len(baseline_elements),
        "added_root_keys": len(root["added"]),
        "removed_root_keys": len(root["removed"]),
        "changed_root_keys": len(root["changed"]),
        "added_elements": len(element["added"]),
        "removed_elements": len(element["removed"]),
        "modified_elements": len(element["modified"]),
    }
    return diff, metrics


def save_bundle(
    problem_ir,
    out_dir: str | Path,
    *,
    include_layout_diff: bool = True,
    baseline_layout_path: str | Path | None = None,
    semantic_options: dict[str, Any] | None = None,
) -> dict[str, Path]:
    """Contract-first bundle output.

    1) serialize -> normalize -> order -> validate -> write (semantic/layout)
    2) optional layout diff generation with same contract pipeline
    """
    out_root = Path(out_dir)
    outputs: dict[str, Path] = {}

    semantic, layout = build_canonical_payloads(
        problem_ir,
        validate=True,
        semantic_options=semantic_options,
    )

    semantic_path = out_root / "json" / "semantic_final" / "semantic_final.json"
    _write_json(semantic_path, semantic)
    outputs["semantic"] = semantic_path

    layout_path = out_root / "json" / "layout_final" / "layout_final.json"
    _write_json(layout_path, layout)
    outputs["layout"] = layout_path

    if include_layout_diff and baseline_layout_path is not None:
        baseline = _read_json(Path(baseline_layout_path))
        diff, metrics = _build_layout_diff(layout, baseline)
        layout_diff = serialize_layout_diff(
            problem_ir.problem_id,
            diff=diff,
            metrics=metrics,
            metadata={"generator": "modu_semantic.output.save_bundle", "baseline": str(baseline_layout_path)},
        )
        layout_diff = normalize_layout_diff(layout_diff)
        layout_diff = order_layout_diff(layout_diff)
        validate_layout_diff(layout_diff)

        layout_diff_path = out_root / "json" / "layout_final" / "layout_diff.json"
        _write_json(layout_diff_path, layout_diff)
        outputs["layout_diff"] = layout_diff_path

    return outputs
