from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _to_num(value: str) -> float | int | str:
    raw = value.strip()
    for suffix in ("px", "pt", "em", "rem", "%"):
        if raw.endswith(suffix):
            raw = raw[: -len(suffix)]
            break
    try:
        f = float(raw)
        return int(round(f)) if abs(f - round(f)) < 1e-9 else f
    except ValueError:
        return value


def _build_element_from_svg_node(
    node: ET.Element,
    attr_map: dict[str, str],
    numeric: set[str],
) -> dict[str, Any] | None:
    tag = _strip_ns(node.tag)
    if tag not in {"text", "rect", "line", "circle", "polygon"}:
        return None

    attrs = dict(node.attrib)
    normalized: dict[str, Any] = {}
    for k, v in attrs.items():
        normalized[attr_map.get(k, k.replace("-", "_"))] = v

    elem_id = normalized.get("id")
    if not elem_id:
        return None

    elem: dict[str, Any] = {
        "id": elem_id,
        "type": tag,
        "semantic_role": "decorative",
        "group": "default",
    }
    for k, v in normalized.items():
        if k == "id":
            continue
        if k in numeric:
            elem[k] = _to_num(v)
        else:
            elem[k] = v

    if tag == "text":
        elem["text"] = "".join(node.itertext()).strip()

    return elem


def build_semantic_edit_from_svg(base_semantic_json: Path, edit_svg: Path, out_json: Path) -> Path:
    base = json.loads(base_semantic_json.read_text(encoding="utf-8"))
    root = ET.parse(edit_svg).getroot()

    svg_by_id: dict[str, ET.Element] = {}
    for node in root.iter():
        tag = _strip_ns(node.tag)
        if tag in {"svg", "defs", "namedview"} or ":" in tag:
            continue
        node_id = node.attrib.get("id")
        if node_id:
            svg_by_id[node_id] = node

    attr_map = {
        "font-family": "font_family",
        "font-size": "font_size",
        "stroke-width": "stroke_width",
        "text-anchor": "anchor",
        "font-weight": "font_weight",
    }
    numeric = {
        "x",
        "y",
        "x1",
        "y1",
        "x2",
        "y2",
        "width",
        "height",
        "rx",
        "ry",
        "r",
        "cx",
        "cy",
        "stroke_width",
        "font_size",
    }

    kept_elements: list[dict[str, Any]] = []
    removed_element_ids: list[str] = []

    used_ids: set[str] = set()

    for elem in base.get("elements", []):
        if not isinstance(elem, dict):
            kept_elements.append(elem)
            continue
        elem_id = elem.get("id")
        if not elem_id:
            kept_elements.append(elem)
            continue
        node = svg_by_id.get(elem_id)
        if node is None:
            removed_element_ids.append(elem_id)
            continue
        used_ids.add(elem_id)

        attrs = dict(node.attrib)
        normalized: dict[str, Any] = {}
        for k, v in attrs.items():
            normalized[attr_map.get(k, k.replace("-", "_"))] = v

        for k, v in normalized.items():
            if k == "id":
                continue
            if k in numeric:
                elem[k] = _to_num(v)
            elif k in elem or k in {
                "fill",
                "stroke",
                "anchor",
                "font_family",
                "font_size",
                "font_weight",
                "dasharray",
                "transform",
                "style",
            }:
                elem[k] = v

        if _strip_ns(node.tag) == "text":
            elem["text"] = "".join(node.itertext()).strip()

        kept_elements.append(elem)

    # Include newly added SVG elements that did not exist in stage1 semantic.
    for node_id, node in svg_by_id.items():
        if node_id in used_ids:
            continue
        extra = _build_element_from_svg_node(node, attr_map, numeric)
        if extra is not None:
            kept_elements.append(extra)

    base["elements"] = kept_elements

    meta = base.setdefault("meta", {})
    meta["source_svg"] = str(edit_svg).replace("\\", "/")
    meta["derived_from"] = str(base_semantic_json).replace("\\", "/")
    meta["stage"] = "edit"
    if removed_element_ids:
        meta["removed_element_ids"] = removed_element_ids

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_json
