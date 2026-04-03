from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    for suffix in ("px", "pt", "em", "rem", "%"):
        if raw.endswith(suffix):
            raw = raw[: -len(suffix)]
            break
    try:
        return float(raw)
    except ValueError:
        return None


def _to_num(value: float | None) -> float | int | None:
    if value is None:
        return None
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    return round(value, 6)


def _bbox(tag: str, attrs: dict[str, str]) -> dict[str, float]:
    if tag == "rect":
        x = _to_float(attrs.get("x")) or 0.0
        y = _to_float(attrs.get("y")) or 0.0
        w = _to_float(attrs.get("width")) or 0.0
        h = _to_float(attrs.get("height")) or 0.0
        return {"x": x, "y": y, "width": w, "height": h}
    if tag == "line":
        x1 = _to_float(attrs.get("x1")) or 0.0
        y1 = _to_float(attrs.get("y1")) or 0.0
        x2 = _to_float(attrs.get("x2")) or 0.0
        y2 = _to_float(attrs.get("y2")) or 0.0
        return {"x": min(x1, x2), "y": min(y1, y2), "width": abs(x2 - x1), "height": abs(y2 - y1)}
    if tag == "text":
        x = _to_float(attrs.get("x")) or 0.0
        y = _to_float(attrs.get("y")) or 0.0
        return {"x": x, "y": y, "width": 0.0, "height": 0.0}
    if tag == "circle":
        cx = _to_float(attrs.get("cx")) or 0.0
        cy = _to_float(attrs.get("cy")) or 0.0
        r = _to_float(attrs.get("r")) or 0.0
        return {"x": cx - r, "y": cy - r, "width": 2 * r, "height": 2 * r}
    return {"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}


def extract_layout(svg_path: Path) -> dict[str, Any]:
    root = ET.parse(svg_path).getroot()
    canvas = {
        "width": _to_num(_to_float(root.attrib.get("width"))),
        "height": _to_num(_to_float(root.attrib.get("height"))),
        "viewBox": root.attrib.get("viewBox"),
    }

    elements: list[dict[str, Any]] = []
    count_by_type: dict[str, int] = {}
    for idx, node in enumerate(root.iter()):
        tag = _strip_ns(node.tag)
        if tag == "svg" or tag in {"defs", "namedview"} or ":" in tag:
            continue
        attrs = dict(node.attrib)
        bb = _bbox(tag, attrs)
        item: dict[str, Any] = {
            "index": idx,
            "id": attrs.get("id"),
            "type": tag,
            "x": _to_num(bb["x"]),
            "y": _to_num(bb["y"]),
            "width": _to_num(bb["width"]),
            "height": _to_num(bb["height"]),
            "attrs": attrs,
        }
        if tag == "text":
            item["text"] = "".join(node.itertext()).strip()
        elements.append(item)
        count_by_type[tag] = count_by_type.get(tag, 0) + 1

    return {
        "canvas": canvas,
        "summary": {
            "total_elements": len(elements),
            "count_by_type": dict(sorted(count_by_type.items())),
            "with_id": sum(1 for e in elements if e.get("id")),
            "without_id": sum(1 for e in elements if not e.get("id")),
        },
        "elements": elements,
    }


def write_layout(svg_path: Path, out_path: Path) -> Path:
    layout = extract_layout(svg_path)
    payload = {
        "meta": {
            "source_svg": str(svg_path).replace("\\", "/"),
            "generator": "problem.common.layout_tools.write_layout",
        },
        **layout,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def write_layout_diff(base_svg: Path, edit_svg: Path, out_path: Path) -> Path:
    base = extract_layout(base_svg)
    edit = extract_layout(edit_svg)
    base_by_id = {e["id"]: e for e in base["elements"] if e.get("id")}
    edit_by_id = {e["id"]: e for e in edit["elements"] if e.get("id")}

    base_ids = set(base_by_id)
    edit_ids = set(edit_by_id)
    added = sorted(edit_ids - base_ids)
    removed = sorted(base_ids - edit_ids)
    changed: list[dict[str, Any]] = []
    for elem_id in sorted(base_ids & edit_ids):
        left = base_by_id[elem_id]
        right = edit_by_id[elem_id]
        d: dict[str, Any] = {}
        for key in ("type", "x", "y", "width", "height", "text"):
            if left.get(key) != right.get(key):
                d[key] = {"base": left.get(key), "edit": right.get(key)}
        if d:
            changed.append({"id": elem_id, "changes": d})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "meta": {
                    "base_svg": str(base_svg).replace("\\", "/"),
                    "edit_svg": str(edit_svg).replace("\\", "/"),
                    "generator": "problem.common.layout_tools.write_layout_diff",
                },
                "diff": {
                    "added_ids": added,
                    "removed_ids": removed,
                    "changed_count": len(changed),
                    "changed": changed,
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return out_path
