from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "examples", ROOT / "sample_data"]
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "renderer_optimize_report.json"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _text_attrs(node: dict[str, Any]) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
    attrs["x"] = node.get("x", 0)
    attrs["y"] = node.get("y", 0)
    if "anchor" in node:
        attrs["text-anchor"] = node["anchor"]
    for key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]:
        if key in props:
            attrs[key.replace("_", "-")] = props[key]
    if props.get("is_formula"):
        attrs["data-formula"] = props.get("text", "")
        attrs["class"] = "formula-placeholder"
    return attrs


def _shape_attrs(node: dict[str, Any], shape_type: str) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
    for key in ["fill", "stroke", "stroke_width", "opacity", "transform"]:
        if key in props:
            attrs[key.replace("_", "-")] = props[key]

    if shape_type == "rect":
        attrs["x"] = node.get("x", 0)
        attrs["y"] = node.get("y", 0)
        if "width" in node:
            attrs["width"] = node["width"]
        if "height" in node:
            attrs["height"] = node["height"]
        if "rx" in props:
            attrs["rx"] = props["rx"]
        if "ry" in props:
            attrs["ry"] = props["ry"]
        return attrs

    if shape_type == "circle":
        attrs["cx"] = node.get("x", 0)
        attrs["cy"] = node.get("y", 0)
        if "r" in props:
            attrs["r"] = props["r"]
        return attrs

    if shape_type == "line":
        attrs["x1"] = props.get("x1", node.get("x", 0))
        attrs["y1"] = props.get("y1", node.get("y", 0))
        if "x2" in props:
            attrs["x2"] = props["x2"]
        if "y2" in props:
            attrs["y2"] = props["y2"]
        return attrs

    if shape_type == "polygon":
        if "points" in props:
            attrs["points"] = props["points"]
        return attrs

    attrs["x"] = node.get("x", 0)
    attrs["y"] = node.get("y", 0)
    if "width" in node:
        attrs["width"] = node["width"]
    if "height" in node:
        attrs["height"] = node["height"]
    return attrs


def _renderer_from_layout(layout: dict[str, Any]) -> dict[str, Any]:
    canvas = layout.get("canvas", {}) if isinstance(layout.get("canvas"), dict) else {}
    nodes = layout.get("nodes", [])
    elements: list[dict[str, Any]] = []

    if isinstance(nodes, list):
        ordered_nodes = sorted(
            [n for n in nodes if isinstance(n, dict)],
            key=lambda n: n.get("z_order", 0),
        )
        for node in ordered_nodes:
            nid = str(node.get("id", ""))
            ntype = str(node.get("type", ""))
            props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
            if ntype == "text":
                elements.append(
                    {
                        "id": nid,
                        "type": "text",
                        "attributes": _text_attrs(node),
                        "text": str(props.get("text", "")),
                    }
                )
                continue
            shape_type = str(props.get("shape_type", "shape"))
            elements.append(
                {
                    "id": nid,
                    "type": shape_type,
                    "attributes": _shape_attrs(node, shape_type),
                }
            )

    out: dict[str, Any] = {
        "problem_id": layout.get("problem_id", ""),
        "view_box": {
            "width": canvas.get("width", 0),
            "height": canvas.get("height", 0),
        },
        "elements": elements,
    }
    if "background" in canvas:
        out["view_box"]["background"] = canvas["background"]
    return out


def main() -> None:
    layout_files: list[Path] = []
    for target in TARGET_DIRS:
        if target.exists():
            layout_files.extend(target.rglob("*.layout.json"))

    counts = {
        "layout_files": len(layout_files),
        "renderer_updated": 0,
        "renderer_created": 0,
        "parse_error_count": 0,
    }
    parse_errors: list[str] = []

    for layout_path in layout_files:
        try:
            layout_payload = _load(layout_path)
            if not isinstance(layout_payload, dict):
                continue
            if "nodes" not in layout_payload or "canvas" not in layout_payload:
                continue
            renderer_payload = _renderer_from_layout(layout_payload)
            if not layout_path.name.endswith(".layout.json"):
                continue
            renderer_path = layout_path.with_name(layout_path.name.replace(".layout.json", ".renderer.json"))
            exists = renderer_path.exists()
            _write(renderer_path, renderer_payload)
            if exists:
                counts["renderer_updated"] += 1
            else:
                counts["renderer_created"] += 1
        except Exception as exc:
            parse_errors.append(f"{layout_path}: {exc}")

    counts["parse_error_count"] = len(parse_errors)
    report = {
        "targets": [str(p) for p in TARGET_DIRS],
        "counts": counts,
        "parse_errors_sample": parse_errors[:200],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH={REPORT_PATH}")


if __name__ == "__main__":
    main()
