from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [PROJECT_ROOT / "examples", PROJECT_ROOT / "sample_data"]

SEMANTIC_SCHEMA_PATH = PROJECT_ROOT / "schema" / "semantic" / "semantic.v1.json"
LAYOUT_SCHEMA_PATH = PROJECT_ROOT / "schema" / "layout" / "layout.v1.json"
RENDERER_SCHEMA_PATH = PROJECT_ROOT / "schema" / "renderer" / "renderer.v1.json"
PROFILE_PATH = PROJECT_ROOT / "schema" / "contract" / "canonical_order_profile.json"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_PATH = REPORT_DIR / "json_schema_audit_examples_sample_data.json"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _matches_type(value: Any, schema_type: str) -> bool:
    if schema_type == "object":
        return isinstance(value, dict)
    if schema_type == "array":
        return isinstance(value, list)
    if schema_type == "string":
        return isinstance(value, str)
    if schema_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if schema_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if schema_type == "boolean":
        return isinstance(value, bool)
    return True


def _validate_by_schema(data: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    schema_type = schema.get("type")
    if isinstance(schema_type, str) and not _matches_type(data, schema_type):
        return [f"{path}: expected {schema_type}, got {type(data).__name__}"]

    if isinstance(data, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in data:
                    errors.append(f"{path}: missing required key '{key}'")

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, sub_schema in properties.items():
                if key in data and isinstance(sub_schema, dict):
                    errors.extend(_validate_by_schema(data[key], sub_schema, f"{path}.{key}"))

    if isinstance(data, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(data):
                errors.extend(_validate_by_schema(item, item_schema, f"{path}[{idx}]"))

    return errors


def _order_dict(data: dict[str, Any], order: list[str]) -> dict[str, Any]:
    ordered: dict[str, Any] = {}
    for key in order:
        if key in data:
            ordered[key] = data[key]
    for key, value in data.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def _classify(data: dict[str, Any]) -> str:
    if {"problem_id", "view_box", "elements"}.issubset(data.keys()):
        return "renderer"
    if {"problem_id", "canvas", "nodes"}.issubset(data.keys()):
        return "layout"
    if {"problem_id", "problem_type", "domain", "answer"}.issubset(data.keys()):
        return "semantic"
    if "patches" in data and "problem_id" in data:
        return "layout_diff"
    return "unknown"


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


def _infer_prefix(path: Path, payload: dict[str, Any], suffix: str) -> str:
    if path.name.endswith(suffix):
        return path.name[: -len(suffix)]
    pid = payload.get("problem_id")
    if isinstance(pid, str) and pid.strip():
        return pid.strip()
    return path.stem


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _node_from_semantic_element(element: dict[str, Any]) -> dict[str, Any]:
    etype = str(element.get("type", "shape"))
    node: dict[str, Any] = {
        "id": str(element.get("id", "")),
        "x": element.get("x", element.get("x1", 0.0)),
        "y": element.get("y", element.get("y1", 0.0)),
    }
    if "width" in element:
        node["width"] = element["width"]
    if "height" in element:
        node["height"] = element["height"]
    if "anchor" in element:
        node["anchor"] = element["anchor"]
    if "z_index" in element:
        node["z_order"] = element["z_index"]

    properties: dict[str, Any] = {}
    skip = {"id", "type", "x", "y", "width", "height", "anchor", "z_index", "alignment"}
    for key, value in element.items():
        if key in skip:
            continue
        properties[key] = value

    if etype in {"text", "formula"}:
        node["type"] = "text"
        if etype == "formula":
            properties["is_formula"] = True
            properties["text"] = element.get("expr", element.get("text", ""))
        else:
            properties["text"] = element.get("text", "")
    else:
        node["type"] = "shape"
        properties["shape_type"] = etype
        if etype == "line":
            node["x"] = element.get("x1", node["x"])
            node["y"] = element.get("y1", node["y"])

    node["properties"] = properties
    return node


def _layout_from_semantic(semantic: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    render = semantic.get("render", {})
    canvas = dict(render.get("canvas", {})) if isinstance(render.get("canvas", {}), dict) else {}
    elements = render.get("elements", [])

    nodes: list[dict[str, Any]] = []
    if isinstance(elements, list):
        for element in elements:
            if isinstance(element, dict):
                nodes.append(_node_from_semantic_element(element))

    if isinstance(profile.get("canvas_order"), list):
        canvas = _order_dict(canvas, list(profile["canvas_order"]))

    layout = {"problem_id": semantic.get("problem_id", ""), "canvas": canvas, "nodes": nodes}
    if isinstance(profile.get("layout_root_order"), list):
        layout = _order_dict(layout, list(profile["layout_root_order"]))
    return layout


def _renderer_element_from_semantic(element: dict[str, Any]) -> dict[str, Any]:
    etype = str(element.get("type", ""))
    attrs: dict[str, Any] = {}
    skip = {"id", "type", "text", "expr", "semantic_role", "z_index", "alignment"}
    for key, value in element.items():
        if key in skip:
            continue
        attrs[key.replace("_", "-")] = value

    out = {"id": str(element.get("id", "")), "type": "text" if etype == "formula" else etype, "attributes": attrs}
    if etype in {"text", "formula"}:
        out["text"] = str(element.get("text", element.get("expr", "")))
    return out


def _renderer_from_semantic(semantic: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    render = semantic.get("render", {})
    canvas = render.get("canvas", {}) if isinstance(render.get("canvas", {}), dict) else {}
    elements = render.get("elements", [])

    out_elements: list[dict[str, Any]] = []
    if isinstance(elements, list):
        for element in elements:
            if isinstance(element, dict):
                out_elements.append(_renderer_element_from_semantic(element))

    view_box = {"width": canvas.get("width", 0), "height": canvas.get("height", 0)}
    if "background" in canvas:
        view_box["background"] = canvas["background"]
    if isinstance(profile.get("view_box_order"), list):
        view_box = _order_dict(view_box, list(profile["view_box_order"]))

    renderer = {"problem_id": semantic.get("problem_id", ""), "view_box": view_box, "elements": out_elements}
    if isinstance(profile.get("renderer_root_order"), list):
        renderer = _order_dict(renderer, list(profile["renderer_root_order"]))
    return renderer


def _legacy_layout_to_canonical(data: dict[str, Any], profile: dict[str, Any], fallback_problem_id: str) -> dict[str, Any]:
    canvas_raw = data.get("canvas", {}) if isinstance(data.get("canvas", {}), dict) else {}
    canvas: dict[str, Any] = {"width": canvas_raw.get("width", 0), "height": canvas_raw.get("height", 0)}
    if "background" in canvas_raw:
        canvas["background"] = canvas_raw["background"]
    if isinstance(profile.get("canvas_order"), list):
        canvas = _order_dict(canvas, list(profile["canvas_order"]))

    nodes: list[dict[str, Any]] = []
    elements = data.get("elements", [])
    if isinstance(elements, list):
        for idx, element in enumerate(elements):
            if not isinstance(element, dict):
                continue
            attrs = element.get("attrs", {}) if isinstance(element.get("attrs"), dict) else {}
            etype = str(element.get("type", "shape"))
            node_id = element.get("id") or f"legacy_{idx + 1}"
            x = element.get("x", attrs.get("x", attrs.get("x1", 0)))
            y = element.get("y", attrs.get("y", attrs.get("y1", 0)))

            node: dict[str, Any] = {"id": str(node_id), "x": _to_number(x), "y": _to_number(y)}
            if "width" in element:
                node["width"] = _to_number(element["width"])
            if "height" in element:
                node["height"] = _to_number(element["height"])

            props: dict[str, Any] = {}
            for key, value in attrs.items():
                props[key.replace("-", "_")] = _to_number(value)
            for key, value in element.items():
                if key in {"index", "id", "type", "x", "y", "width", "height", "attrs"}:
                    continue
                props[key] = value

            if etype in {"text", "formula"}:
                node["type"] = "text"
                if "text" in element:
                    props["text"] = element["text"]
                elif "text" in attrs:
                    props["text"] = attrs["text"]
                if etype == "formula":
                    props["is_formula"] = True
            else:
                node["type"] = "shape"
                props["shape_type"] = etype

            node["properties"] = props
            nodes.append(node)

    layout = {"problem_id": data.get("problem_id", fallback_problem_id), "canvas": canvas, "nodes": nodes}
    if isinstance(profile.get("layout_root_order"), list):
        layout = _order_dict(layout, list(profile["layout_root_order"]))
    return layout


def _renderer_from_layout(layout: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    canvas = layout.get("canvas", {}) if isinstance(layout.get("canvas", {}), dict) else {}
    nodes = layout.get("nodes", [])
    elements: list[dict[str, Any]] = []

    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            nid = str(node.get("id", ""))
            ntype = str(node.get("type", ""))
            props = node.get("properties", {}) if isinstance(node.get("properties", {}), dict) else {}

            attrs: dict[str, Any] = {}
            for key in ("x", "y", "width", "height", "anchor"):
                if key in node:
                    attrs["text-anchor" if key == "anchor" else key] = node[key]
            for key, value in props.items():
                if key in {"shape_type", "text"}:
                    continue
                attrs[key.replace("_", "-")] = value

            if ntype == "text":
                elements.append({"id": nid, "type": "text", "attributes": attrs, "text": str(props.get("text", ""))})
                continue

            shape_type = str(props.get("shape_type", "shape"))
            if shape_type == "circle":
                if "x" in attrs:
                    attrs["cx"] = attrs.pop("x")
                if "y" in attrs:
                    attrs["cy"] = attrs.pop("y")
            if shape_type == "line":
                if "x1" not in attrs and "x" in node:
                    attrs["x1"] = node["x"]
                if "y1" not in attrs and "y" in node:
                    attrs["y1"] = node["y"]
            elements.append({"id": nid, "type": shape_type, "attributes": attrs})

    view_box = {"width": canvas.get("width", 0), "height": canvas.get("height", 0)}
    if "background" in canvas:
        view_box["background"] = canvas["background"]
    if isinstance(profile.get("view_box_order"), list):
        view_box = _order_dict(view_box, list(profile["view_box_order"]))

    renderer = {"problem_id": layout.get("problem_id", ""), "view_box": view_box, "elements": elements}
    if isinstance(profile.get("renderer_root_order"), list):
        renderer = _order_dict(renderer, list(profile["renderer_root_order"]))
    return renderer


def main() -> None:
    semantic_schema = _load_json(SEMANTIC_SCHEMA_PATH)
    layout_schema = _load_json(LAYOUT_SCHEMA_PATH)
    renderer_schema = _load_json(RENDERER_SCHEMA_PATH)
    profile = _load_json(PROFILE_PATH) if PROFILE_PATH.exists() else {}

    all_json_files: list[Path] = []
    for root in TARGET_ROOTS:
        if root.exists():
            all_json_files.extend(root.rglob("*.json"))

    counts = {
        "all_json": len(all_json_files),
        "semantic_detected": 0,
        "layout_detected": 0,
        "renderer_detected": 0,
        "unknown_detected": 0,
        "parse_error": 0,
        "semantic_invalid": 0,
        "layout_invalid": 0,
        "renderer_invalid": 0,
        "normalized_semantic_named": 0,
        "normalized_layout_legacy": 0,
        "generated_layout": 0,
        "generated_renderer": 0,
    }

    invalid_examples: list[dict[str, Any]] = []
    semantic_payloads: list[tuple[Path, dict[str, Any]]] = []
    semantic_index: dict[Path, dict[str, Any]] = {}

    for path in all_json_files:
        try:
            payload = _load_json(path)
        except Exception as exc:
            counts["parse_error"] += 1
            if len(invalid_examples) < 200:
                invalid_examples.append({"path": str(path), "kind": "parse_error", "error": str(exc)})
            continue

        if not isinstance(payload, dict):
            counts["unknown_detected"] += 1
            continue

        kind = _classify(payload)
        if kind == "semantic":
            counts["semantic_detected"] += 1
            errs = _validate_by_schema(payload, semantic_schema)
            if errs:
                counts["semantic_invalid"] += 1
                if len(invalid_examples) < 200:
                    invalid_examples.append({"path": str(path), "kind": "semantic", "errors": errs[:5]})
            semantic_payloads.append((path, payload))
            semantic_index[path] = payload
        elif kind == "layout":
            counts["layout_detected"] += 1
            errs = _validate_by_schema(payload, layout_schema)
            if errs:
                counts["layout_invalid"] += 1
                if len(invalid_examples) < 200:
                    invalid_examples.append({"path": str(path), "kind": "layout", "errors": errs[:5]})
        elif kind == "renderer":
            counts["renderer_detected"] += 1
            errs = _validate_by_schema(payload, renderer_schema)
            if errs:
                counts["renderer_invalid"] += 1
                if len(invalid_examples) < 200:
                    invalid_examples.append({"path": str(path), "kind": "renderer", "errors": errs[:5]})
        else:
            counts["unknown_detected"] += 1

    # Semantic naming normalization and generation
    for path, semantic in semantic_payloads:
        prefix = _infer_prefix(path, semantic, ".semantic.json")
        canonical_semantic = path.parent / f"{prefix}.semantic.json"
        if canonical_semantic != path and not canonical_semantic.exists():
            _write_json(canonical_semantic, semantic)
            counts["normalized_semantic_named"] += 1
            semantic_index[canonical_semantic] = semantic

        layout_path = path.parent / f"{prefix}.layout.json"
        if not layout_path.exists():
            layout_payload = _layout_from_semantic(semantic, profile)
            if not _validate_by_schema(layout_payload, layout_schema):
                _write_json(layout_path, layout_payload)
                counts["generated_layout"] += 1

        renderer_path = path.parent / f"{prefix}.renderer.json"
        if not renderer_path.exists():
            renderer_payload = _renderer_from_semantic(semantic, profile)
            if not _validate_by_schema(renderer_payload, renderer_schema):
                _write_json(renderer_path, renderer_payload)
                counts["generated_renderer"] += 1

    # Legacy layout normalization
    for layout_path in [p for p in all_json_files if p.name.endswith(".layout.json")]:
        try:
            layout_payload = _load_json(layout_path)
        except Exception:
            continue
        if not isinstance(layout_payload, dict):
            continue

        if not _validate_by_schema(layout_payload, layout_schema):
            continue

        prefix = layout_path.name[: -len(".layout.json")]
        semantic_path = layout_path.parent / f"{prefix}.semantic.json"
        semantic_payload = semantic_index.get(semantic_path) if semantic_path.exists() else None

        if isinstance(semantic_payload, dict):
            normalized_layout = _layout_from_semantic(semantic_payload, profile)
        else:
            normalized_layout = _legacy_layout_to_canonical(layout_payload, profile, prefix)

        if not _validate_by_schema(normalized_layout, layout_schema):
            _write_json(layout_path, normalized_layout)
            counts["normalized_layout_legacy"] += 1

        renderer_path = layout_path.parent / f"{prefix}.renderer.json"
        if not renderer_path.exists():
            renderer_payload = _renderer_from_layout(normalized_layout, profile)
            if not _validate_by_schema(renderer_payload, renderer_schema):
                _write_json(renderer_path, renderer_payload)
                counts["generated_renderer"] += 1

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "targets": [str(root) for root in TARGET_ROOTS],
        "counts": counts,
        "invalid_examples_limited": invalid_examples,
    }
    _write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH={REPORT_PATH}")


if __name__ == "__main__":
    main()
