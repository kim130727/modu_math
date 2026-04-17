from __future__ import annotations

from typing import Any

from .contracts import load_contract_json


class SchemaValidationError(ValueError):
    pass


_ALLOWED_TYPES = {"rect", "circle", "line", "polygon", "text", "formula"}
_ALLOWED_ANCHORS = {"start", "middle", "end"}
_ALLOWED_ALIGNMENTS = {"left", "center", "right"}

_REQUIRED_FIELDS_BY_TYPE = {
    "rect": {"x", "y", "width", "height"},
    "circle": {"x", "y", "r"},
    "line": {"x1", "y1", "x2", "y2"},
    "polygon": {"points"},
    "text": {"x", "y", "text"},
    "formula": {"x", "y", "expr"},
}

_NUMERIC_FIELDS_BY_TYPE = {
    "rect": {"x", "y", "width", "height", "rx", "ry", "stroke_width", "font_size", "z_index"},
    "circle": {"x", "y", "r", "stroke_width", "font_size", "z_index"},
    "line": {"x1", "y1", "x2", "y2", "stroke_width", "font_size", "z_index"},
    "polygon": {"stroke_width", "font_size", "z_index"},
    "text": {"x", "y", "stroke_width", "font_size", "z_index"},
    "formula": {"x", "y", "stroke_width", "font_size", "z_index"},
}

_FORBIDDEN_FIELD_COMBINATIONS = {
    "text": {"expr"},
    "formula": {"text"},
}


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _is_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    return True


def _is_number(value: Any) -> bool:
    return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)


def _validate_schema(value: Any, schema: dict[str, Any], path: str) -> None:
    if "const" in schema and value != schema["const"]:
        raise SchemaValidationError(f"{path} must be {schema['const']!r}, got {value!r}")

    if "enum" in schema and value not in schema["enum"]:
        raise SchemaValidationError(f"{path} must be one of {schema['enum']}, got {value!r}")

    expected_type = schema.get("type")
    if expected_type is not None:
        if isinstance(expected_type, list):
            if not any(_is_type(value, t) for t in expected_type):
                raise SchemaValidationError(f"{path} must be one of types {expected_type}, got {type(value).__name__}")
        else:
            if not _is_type(value, expected_type):
                raise SchemaValidationError(f"{path} must be type {expected_type}, got {type(value).__name__}")

    if isinstance(value, dict):
        props = schema.get("properties", {})
        required = schema.get("required", [])

        for req_key in required:
            if req_key not in value:
                raise SchemaValidationError(f"Missing required key at {path}: {req_key}")

        additional = schema.get("additionalProperties", True)
        if additional is False:
            unknown = [k for k in value.keys() if k not in props]
            if unknown:
                raise SchemaValidationError(f"Unexpected key at {path}: {unknown[0]}")

        for key, child in value.items():
            child_schema = props.get(key)
            if child_schema is None:
                if isinstance(additional, dict):
                    _validate_schema(child, additional, f"{path}.{key}")
                continue
            _validate_schema(child, child_schema, f"{path}.{key}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            raise SchemaValidationError(f"{path} must contain at least {min_items} items, got {len(value)}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(value):
                _validate_schema(item, item_schema, f"{path}[{idx}]")

    all_of = schema.get("allOf")
    if isinstance(all_of, list):
        for idx, sub_schema in enumerate(all_of):
            if isinstance(sub_schema, dict):
                _validate_schema(value, sub_schema, f"{path}.allOf[{idx}]")

    if_schema = schema.get("if")
    if isinstance(if_schema, dict):
        if _schema_matches(value, if_schema, path):
            then_schema = schema.get("then")
            if isinstance(then_schema, dict):
                _validate_schema(value, then_schema, path)
        else:
            else_schema = schema.get("else")
            if isinstance(else_schema, dict):
                _validate_schema(value, else_schema, path)


def _schema_matches(value: Any, schema: dict[str, Any], path: str) -> bool:
    try:
        _validate_schema(value, schema, path)
        return True
    except SchemaValidationError:
        return False


def _validate_root_order(data: dict[str, Any], expected: list[str], path: str) -> None:
    present_expected = [k for k in expected if k in data]
    actual_prefix = list(data.keys())[: len(present_expected)]
    if actual_prefix != present_expected:
        raise SchemaValidationError(
            f"{path} root key order mismatch: expected prefix {present_expected}, got {actual_prefix}"
        )


def _validate_semantic_elements(data: dict[str, Any]) -> None:
    render = data["render"]
    canvas = render["canvas"]
    elements = render["elements"]

    _ensure(isinstance(canvas, dict), "render.canvas must be an object")
    _ensure(isinstance(elements, list), "render.elements must be an array")

    for idx, element in enumerate(elements):
        _ensure(isinstance(element, dict), f"render.elements[{idx}] must be an object")
        _ensure("id" in element, f"render.elements[{idx}].id is required")
        _ensure("type" in element, f"render.elements[{idx}].type is required")

        etype = element["type"]
        _ensure(etype in _ALLOWED_TYPES, f"render.elements[{idx}].type must be one of {_ALLOWED_TYPES}")

        required_fields = _REQUIRED_FIELDS_BY_TYPE[etype]
        for field_name in required_fields:
            _ensure(field_name in element, f"render.elements[{idx}].{field_name} is required for type '{etype}'")

        for forbidden in _FORBIDDEN_FIELD_COMBINATIONS.get(etype, set()):
            _ensure(
                forbidden not in element,
                f"render.elements[{idx}] type '{etype}' cannot include '{forbidden}'",
            )

        for num_field in _NUMERIC_FIELDS_BY_TYPE[etype]:
            if num_field in element:
                _ensure(
                    _is_number(element[num_field]),
                    f"render.elements[{idx}].{num_field} must be numeric",
                )

        if etype == "polygon":
            points = element.get("points")
            _ensure(isinstance(points, list), f"render.elements[{idx}].points must be an array")
            _ensure(len(points) >= 3, f"render.elements[{idx}].points must contain at least 3 points")
            for point_idx, point in enumerate(points):
                _ensure(
                    isinstance(point, list) and len(point) == 2 and all(_is_number(v) for v in point),
                    f"render.elements[{idx}].points[{point_idx}] must be [number, number]",
                )

        if "id" in element:
            _ensure(isinstance(element["id"], str), f"render.elements[{idx}].id must be string")

        if "anchor" in element:
            _ensure(
                element["anchor"] in _ALLOWED_ANCHORS,
                f"render.elements[{idx}].anchor must be one of {_ALLOWED_ANCHORS}",
            )
        if "alignment" in element:
            _ensure(
                element["alignment"] in _ALLOWED_ALIGNMENTS,
                f"render.elements[{idx}].alignment must be one of {_ALLOWED_ALIGNMENTS}",
            )


def validate_semantic_json(data: dict[str, Any]) -> None:
    schema = load_contract_json("semantic_v3.schema.json")
    _validate_schema(data, schema, "$")

    profile = load_contract_json("canonical_order_profile.json")
    semantic_order = profile.get("semantic_root_order")
    if isinstance(semantic_order, list):
        _validate_root_order(data, semantic_order, "semantic")

    render = data.get("render", {})
    if isinstance(render, dict):
        render_order = profile.get("render_order")
        if isinstance(render_order, list):
            _validate_root_order(render, render_order, "semantic.render")
        canvas = render.get("canvas", {})
        if isinstance(canvas, dict):
            canvas_order = profile.get("canvas_order")
            if isinstance(canvas_order, list):
                _validate_root_order(canvas, canvas_order, "semantic.render.canvas")

    answer = data.get("answer", {})
    if isinstance(answer, dict):
        answer_order = profile.get("answer_order")
        if isinstance(answer_order, list):
            _validate_root_order(answer, answer_order, "semantic.answer")

    _validate_semantic_elements(data)


def validate_layout_json(data: dict[str, Any]) -> None:
    schema = load_contract_json("layout_v1.schema.json")
    _validate_schema(data, schema, "$")
    profile = load_contract_json("canonical_order_profile.json")
    _validate_root_order(data, profile["layout_root_order"], "layout")


def validate_layout_diff_json(data: dict[str, Any]) -> None:
    schema = load_contract_json("layout_diff_v1.schema.json")
    _validate_schema(data, schema, "$")
    profile = load_contract_json("canonical_order_profile.json")
    _validate_root_order(data, profile["layout_diff_root_order"], "layout_diff")
