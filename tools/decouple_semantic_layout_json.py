from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "examples", ROOT / "sample_data"]
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "decouple_semantic_layout_report.json"


VISUAL_KEYS = {
    "x",
    "y",
    "x1",
    "y1",
    "x2",
    "y2",
    "cx",
    "cy",
    "r",
    "rx",
    "ry",
    "width",
    "height",
    "points",
    "path",
    "d",
    "anchor",
    "alignment",
    "z_index",
    "z_order",
    "fill",
    "stroke",
    "stroke_width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke_dasharray",
    "stroke-dasharray",
    "font_family",
    "font_size",
    "font_weight",
    "font_style",
    "font-family",
    "font-size",
    "font-weight",
    "font-style",
    "opacity",
    "transform",
    "background",
    "viewBox",
    "style",
}

SEMANTIC_ONLY_KEYS = {
    "semantic_role",
    "answer_ref",
    "domain_ref",
    "question_ref",
    "is_correct",
    "correct",
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _to_number(value: Any) -> Any:
    if isinstance(value, (int, float)):
        return value
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return value
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return value


def _semantic_clean_render_elements(elements: Any) -> tuple[list[dict[str, Any]], int]:
    cleaned: list[dict[str, Any]] = []
    dropped = 0
    if not isinstance(elements, list):
        return cleaned, dropped
    for elem in elements:
        if not isinstance(elem, dict):
            continue
        out: dict[str, Any] = {}
        for key, value in elem.items():
            if key in VISUAL_KEYS:
                dropped += 1
                continue
            out[key] = value
        cleaned.append(out)
    return cleaned, dropped


def _convert_legacy_layout_elements(elements: list[Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for idx, elem in enumerate(elements):
        if not isinstance(elem, dict):
            continue
        attrs = elem.get("attrs", {}) if isinstance(elem.get("attrs"), dict) else {}
        etype = str(elem.get("type", "shape"))
        node_id = elem.get("id") or f"legacy_{idx + 1}"
        x = elem.get("x", attrs.get("x", attrs.get("x1", 0)))
        y = elem.get("y", attrs.get("y", attrs.get("y1", 0)))

        node: dict[str, Any] = {"id": str(node_id), "x": _to_number(x), "y": _to_number(y)}
        if "width" in elem:
            node["width"] = _to_number(elem["width"])
        if "height" in elem:
            node["height"] = _to_number(elem["height"])

        props: dict[str, Any] = {}
        for key, value in attrs.items():
            nk = key.replace("-", "_")
            if nk in SEMANTIC_ONLY_KEYS:
                continue
            props[nk] = _to_number(value)

        for key, value in elem.items():
            if key in {"index", "id", "type", "x", "y", "width", "height", "attrs"}:
                continue
            if key in SEMANTIC_ONLY_KEYS:
                continue
            props[key] = value

        if etype in {"text", "formula"}:
            node["type"] = "text"
            if "text" in elem:
                props["text"] = elem["text"]
            elif "text" in attrs:
                props["text"] = attrs["text"]
            if etype == "formula":
                props["is_formula"] = True
        else:
            node["type"] = "shape"
            props["shape_type"] = etype

        if props:
            node["properties"] = props
        nodes.append(node)
    return nodes


def _sanitize_layout_nodes(nodes: Any) -> tuple[list[dict[str, Any]], int]:
    out_nodes: list[dict[str, Any]] = []
    removed = 0
    if not isinstance(nodes, list):
        return out_nodes, removed

    for node in nodes:
        if not isinstance(node, dict):
            continue
        out_node = dict(node)
        props = dict(out_node.get("properties", {})) if isinstance(out_node.get("properties"), dict) else {}
        for k in list(props.keys()):
            if k in SEMANTIC_ONLY_KEYS:
                props.pop(k, None)
                removed += 1
        if props:
            out_node["properties"] = props
        elif "properties" in out_node:
            out_node.pop("properties", None)
        out_nodes.append(out_node)
    return out_nodes, removed


def _classify(payload: dict[str, Any]) -> str:
    keys = set(payload.keys())
    if {"problem_id", "problem_type", "domain", "answer"}.issubset(keys):
        return "semantic"
    if {"problem_id", "canvas", "nodes"}.issubset(keys):
        return "layout"
    if {"problem_id", "canvas", "elements"}.issubset(keys):
        return "layout_legacy"
    return "unknown"


def _decouple_semantic(payload: dict[str, Any]) -> tuple[dict[str, Any], int, bool]:
    changed = False
    removed = 0
    out = dict(payload)
    render = out.get("render")
    if isinstance(render, dict):
        new_render = dict(render)
        if "canvas" in new_render:
            new_render.pop("canvas", None)
            changed = True
            removed += 1
        if "elements" in new_render:
            cleaned_elements, dropped = _semantic_clean_render_elements(new_render.get("elements"))
            if dropped > 0 or cleaned_elements != new_render.get("elements"):
                new_render["elements"] = cleaned_elements
                changed = True
                removed += dropped
        out["render"] = new_render
    return out, removed, changed


def _decouple_layout(payload: dict[str, Any]) -> tuple[dict[str, Any], int, bool]:
    removed = 0
    changed = False

    problem_id = payload.get("problem_id", "")
    canvas = payload.get("canvas", {}) if isinstance(payload.get("canvas"), dict) else {}
    nodes = payload.get("nodes")

    if not isinstance(nodes, list):
        legacy_elements = payload.get("elements")
        if isinstance(legacy_elements, list):
            nodes = _convert_legacy_layout_elements(legacy_elements)
            changed = True
            removed += 1
        else:
            nodes = []

    sanitized_nodes, removed_semantic_props = _sanitize_layout_nodes(nodes)
    removed += removed_semantic_props
    if sanitized_nodes != nodes:
        changed = True

    out: dict[str, Any] = {
        "problem_id": problem_id,
        "canvas": canvas,
        "nodes": sanitized_nodes,
    }
    if out != payload:
        changed = True

    return out, removed, changed


def main() -> None:
    semantic_files: list[Path] = []
    layout_files: list[Path] = []
    parse_errors: list[str] = []

    all_json_files: list[Path] = []
    for base in TARGET_DIRS:
        if not base.exists():
            continue
        all_json_files.extend(base.rglob("*.json"))

    for path in all_json_files:
        try:
            payload = _load_json(path)
        except Exception as exc:
            parse_errors.append(f"{path}: {exc}")
            continue
        if not isinstance(payload, dict):
            continue
        kind = _classify(payload)
        if kind == "semantic":
            semantic_files.append(path)
        elif kind in {"layout", "layout_legacy"}:
            layout_files.append(path)

    counts = {
        "semantic_files": len(semantic_files),
        "layout_files": len(layout_files),
        "semantic_changed": 0,
        "layout_changed": 0,
        "semantic_removed_visual_fields": 0,
        "layout_removed_semantic_fields": 0,
        "parse_error_count": 0,
    }

    for path in semantic_files:
        try:
            payload = _load_json(path)
            if not isinstance(payload, dict):
                continue
            decoupled, removed, changed = _decouple_semantic(payload)
            counts["semantic_removed_visual_fields"] += removed
            if changed:
                _write_json(path, decoupled)
                counts["semantic_changed"] += 1
        except Exception as exc:
            parse_errors.append(f"{path}: {exc}")

    for path in layout_files:
        try:
            payload = _load_json(path)
            if not isinstance(payload, dict):
                continue
            decoupled, removed, changed = _decouple_layout(payload)
            counts["layout_removed_semantic_fields"] += removed
            if changed:
                _write_json(path, decoupled)
                counts["layout_changed"] += 1
        except Exception as exc:
            parse_errors.append(f"{path}: {exc}")

    counts["parse_error_count"] = len(parse_errors)

    report = {
        "targets": [str(p) for p in TARGET_DIRS],
        "counts": counts,
        "parse_errors_sample": parse_errors[:200],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH={REPORT_PATH}")


if __name__ == "__main__":
    main()
