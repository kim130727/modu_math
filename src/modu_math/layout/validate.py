from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LayoutValidationError(Exception):
    pass


def _require_non_empty_string(data: dict[str, Any], key: str, path: str = "$") -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise LayoutValidationError(f"{path}.{key} must be a non-empty string")
    return value


def _require_number(data: dict[str, Any], key: str, path: str = "$") -> float:
    value = data.get(key)
    if not isinstance(value, int | float):
        raise LayoutValidationError(f"{path}.{key} must be a number")
    return float(value)


def _validate_node(node: dict[str, Any], path: str) -> None:
    _require_non_empty_string(node, "id", path=path)
    node_type = _require_non_empty_string(node, "type", path=path)
    _require_number(node, "x", path=path)
    _require_number(node, "y", path=path)

    source_ref = node.get("source_ref")
    if source_ref is not None and (not isinstance(source_ref, str) or not source_ref.strip()):
        raise LayoutValidationError(f"{path}.source_ref must be a non-empty string when present")

    if "width" in node and node["width"] is not None and not isinstance(node["width"], int | float):
        raise LayoutValidationError(f"{path}.width must be a number when present")
    if "height" in node and node["height"] is not None and not isinstance(node["height"], int | float):
        raise LayoutValidationError(f"{path}.height must be a number when present")
    if "z_order" in node and not isinstance(node["z_order"], int):
        raise LayoutValidationError(f"{path}.z_order must be an integer when present")
    if "properties" in node and not isinstance(node["properties"], dict):
        raise LayoutValidationError(f"{path}.properties must be an object when present")

    properties = node.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}
    if node_type == "text":
        text = properties.get("text")
        if not isinstance(text, str):
            raise LayoutValidationError(f"{path}.properties.text must be a string for text nodes")
    if node_type == "shape":
        shape_type = properties.get("shape_type")
        if not isinstance(shape_type, str) or not shape_type.strip():
            raise LayoutValidationError(f"{path}.properties.shape_type must be a non-empty string for shape nodes")

def _validate_region(region: dict[str, Any], path: str) -> list[str]:
    _require_non_empty_string(region, "id", path=path)
    _require_non_empty_string(region, "role", path=path)
    _require_non_empty_string(region, "flow", path=path)

    slot_ids = region.get("slot_ids")
    if not isinstance(slot_ids, list):
        raise LayoutValidationError(f"{path}.slot_ids must be an array")

    parsed_ids: list[str] = []
    for idx, slot_id in enumerate(slot_ids):
        if not isinstance(slot_id, str) or not slot_id.strip():
            raise LayoutValidationError(f"{path}.slot_ids[{idx}] must be a non-empty string")
        parsed_ids.append(slot_id)
    return parsed_ids


def _validate_slot(slot: dict[str, Any], path: str) -> None:
    _require_non_empty_string(slot, "id", path=path)
    kind = _require_non_empty_string(slot, "kind", path=path)
    prompt = slot.get("prompt")
    if not isinstance(prompt, str):
        raise LayoutValidationError(f"{path}.prompt must be a string")

    content = slot.get("content")
    if not isinstance(content, dict):
        raise LayoutValidationError(f"{path}.content must be an object")

    # Type-aware minimum checks for common slot kinds.
    if kind == "text":
        text = content.get("text")
        if not isinstance(text, str):
            raise LayoutValidationError(f"{path}.content.text must be a string for text slots")
    if kind == "rect":
        for key in ("x", "y", "width", "height"):
            value = content.get(key)
            if not isinstance(value, int | float):
                raise LayoutValidationError(f"{path}.content.{key} must be a number for rect slots")
    if kind == "line":
        for key in ("x1", "y1", "x2", "y2"):
            value = content.get(key)
            if not isinstance(value, int | float):
                raise LayoutValidationError(f"{path}.content.{key} must be a number for line slots")
    if kind == "circle":
        for key in ("cx", "cy", "r"):
            value = content.get(key)
            if not isinstance(value, int | float):
                raise LayoutValidationError(f"{path}.content.{key} must be a number for circle slots")


def validate_layout_json(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise LayoutValidationError("layout payload must be an object")

    _require_non_empty_string(data, "problem_id")

    canvas = data.get("canvas")
    if not isinstance(canvas, dict):
        raise LayoutValidationError("$.canvas must be an object")
    width = _require_number(canvas, "width", path="$.canvas")
    height = _require_number(canvas, "height", path="$.canvas")
    if width <= 0 or height <= 0:
        raise LayoutValidationError("$.canvas.width and $.canvas.height must be > 0")
    if "background" in canvas and canvas["background"] is not None and not isinstance(canvas["background"], str):
        raise LayoutValidationError("$.canvas.background must be a string when present")

    # Canonical layout v1: regions/slots structure.
    has_regions_or_slots = "regions" in data or "slots" in data
    if has_regions_or_slots:
        schema_name = data.get("schema")
        if schema_name is not None and schema_name != "modu.layout.v1":
            raise LayoutValidationError("$.schema must be 'modu.layout.v1' when present")

        regions = data.get("regions")
        if not isinstance(regions, list):
            raise LayoutValidationError("$.regions must be an array")
        slots = data.get("slots")
        if not isinstance(slots, list):
            raise LayoutValidationError("$.slots must be an array")

        slot_ids: set[str] = set()
        for index, slot in enumerate(slots):
            path = f"$.slots[{index}]"
            if not isinstance(slot, dict):
                raise LayoutValidationError(f"{path} must be an object")
            _validate_slot(slot, path)
            slot_id = str(slot.get("id"))
            if slot_id in slot_ids:
                raise LayoutValidationError(f"{path}.id duplicates existing slot id '{slot_id}'")
            slot_ids.add(slot_id)

        region_ids: set[str] = set()
        referenced_slot_ids: set[str] = set()
        for index, region in enumerate(regions):
            path = f"$.regions[{index}]"
            if not isinstance(region, dict):
                raise LayoutValidationError(f"{path} must be an object")
            region_slot_ids = _validate_region(region, path)
            region_id = str(region.get("id"))
            if region_id in region_ids:
                raise LayoutValidationError(f"{path}.id duplicates existing region id '{region_id}'")
            region_ids.add(region_id)
            for slot_id in region_slot_ids:
                if slot_id not in slot_ids:
                    raise LayoutValidationError(f"{path}.slot_ids contains unknown slot id '{slot_id}'")
                referenced_slot_ids.add(slot_id)

        reading_order = data.get("reading_order")
        if reading_order is not None:
            if not isinstance(reading_order, list):
                raise LayoutValidationError("$.reading_order must be an array when present")
            for idx, item in enumerate(reading_order):
                if not isinstance(item, str) or not item.strip():
                    raise LayoutValidationError(f"$.reading_order[{idx}] must be a non-empty string")

        for key in ("groups", "constraints", "diagrams"):
            value = data.get(key)
            if value is not None and not isinstance(value, list):
                raise LayoutValidationError(f"$.{key} must be an array when present")
        return

    # Legacy compatibility: nodes structure.
    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        raise LayoutValidationError("$.nodes must be an array")

    ids: set[str] = set()
    for index, node in enumerate(nodes):
        path = f"$.nodes[{index}]"
        if not isinstance(node, dict):
            raise LayoutValidationError(f"{path} must be an object")
        _validate_node(node, path)
        node_id = str(node.get("id"))
        if node_id in ids:
            raise LayoutValidationError(f"{path}.id duplicates existing node id '{node_id}'")
        ids.add(node_id)


def load_and_validate_layout(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_layout_json(data)
    return data
