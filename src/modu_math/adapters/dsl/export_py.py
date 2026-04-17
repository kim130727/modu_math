from __future__ import annotations

from pprint import pformat
from typing import Any


def _py_literal(value: Any) -> str:
    return pformat(value, width=120, sort_dicts=False)


def _semantic_role_map(semantic: dict[str, Any]) -> dict[str, str]:
    render = semantic.get("render")
    if not isinstance(render, dict):
        return {}
    elements = render.get("elements")
    if not isinstance(elements, list):
        return {}
    out: dict[str, str] = {}
    for element in elements:
        if not isinstance(element, dict):
            continue
        element_id = element.get("id")
        semantic_role = element.get("semantic_role")
        if isinstance(element_id, str) and isinstance(semantic_role, str) and semantic_role:
            out[element_id] = semantic_role
    return out


def _common_style_kwargs(props: dict[str, Any], *, text_like: bool = False) -> list[tuple[str, Any]]:
    pairs: list[tuple[str, Any]] = []
    for key in ["fill", "stroke", "stroke_width", "opacity", "transform"]:
        if key in props:
            pairs.append((key, props[key]))
    if text_like:
        for key in ["font_family", "font_size", "font_weight", "font_style"]:
            if key in props:
                pairs.append((key, props[key]))
    return pairs


def _node_to_dsl_call(node: dict[str, Any], semantic_role: str | None = None) -> str | None:
    node_id = str(node.get("id", ""))
    node_type = str(node.get("type", ""))
    props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
    z_order = node.get("z_order")

    kwargs: list[tuple[str, Any]] = [("id", node_id)]
    if semantic_role:
        kwargs.append(("semantic_role", semantic_role))
    if isinstance(z_order, int):
        kwargs.append(("z_order", z_order))

    if node_type == "text":
        is_formula = bool(props.get("is_formula"))
        ctor = "Formula" if is_formula else "Text"
        kwargs.extend(
            [
                ("x", node.get("x", 0)),
                ("y", node.get("y", 0)),
            ]
        )
        if is_formula:
            kwargs.append(("expr", str(props.get("text", ""))))
        else:
            kwargs.append(("text", str(props.get("text", ""))))
        if node.get("anchor") is not None:
            kwargs.append(("anchor", node.get("anchor")))
        kwargs.extend(_common_style_kwargs(props, text_like=True))
        args = ", ".join(f"{k}={_py_literal(v)}" for k, v in kwargs)
        return f"    p.add({ctor}({args}))"

    shape_type = str(props.get("shape_type", ""))
    if shape_type == "rect":
        ctor = "Rect"
        kwargs.extend(
            [
                ("x", node.get("x", 0)),
                ("y", node.get("y", 0)),
                ("width", node.get("width", 0)),
                ("height", node.get("height", 0)),
            ]
        )
        if "rx" in props:
            kwargs.append(("rx", props["rx"]))
        if "ry" in props:
            kwargs.append(("ry", props["ry"]))
    elif shape_type == "circle":
        ctor = "Circle"
        kwargs.extend(
            [
                ("cx", node.get("x", 0)),
                ("cy", node.get("y", 0)),
                ("r", props.get("r", 0)),
            ]
        )
    elif shape_type == "line":
        ctor = "Line"
        kwargs.extend(
            [
                ("x1", props.get("x1", node.get("x", 0))),
                ("y1", props.get("y1", node.get("y", 0))),
                ("x2", props.get("x2", node.get("x", 0))),
                ("y2", props.get("y2", node.get("y", 0))),
            ]
        )
    elif shape_type == "polygon":
        ctor = "Polygon"
        kwargs.append(("points", props.get("points", [])))
    else:
        return None

    kwargs.extend(_common_style_kwargs(props, text_like=False))
    args = ", ".join(f"{k}={_py_literal(v)}" for k, v in kwargs)
    return f"    p.add({ctor}({args}))"


def build_generated_py_template(
    *,
    semantic: dict[str, Any],
    layout: dict[str, Any],
    renderer: dict[str, Any],
    source_semantic_name: str = "semantic.json",
    source_layout_name: str = "layout.json",
    source_renderer_name: str = "renderer.json",
) -> str:
    problem_id = str(semantic.get("problem_id") or layout.get("problem_id") or renderer.get("problem_id") or "problem")
    problem_type = str(semantic.get("problem_type", "generic"))
    metadata = semantic.get("metadata", {})
    domain = semantic.get("domain", {})
    answer = semantic.get("answer", {"blanks": [], "choices": [], "answer_key": []})
    renderer_payload = renderer if isinstance(renderer, dict) else {}

    canvas = layout.get("canvas", {}) if isinstance(layout.get("canvas"), dict) else {}
    width = canvas.get("width", 1200)
    height = canvas.get("height", 700)
    background = canvas.get("background", "#F6F6F6")
    nodes = layout.get("nodes", []) if isinstance(layout.get("nodes"), list) else []
    role_map = _semantic_role_map(semantic)

    sorted_nodes = sorted(
        [node for node in nodes if isinstance(node, dict)],
        key=lambda node: int(node.get("z_order", 0)) if isinstance(node.get("z_order", 0), int) else 0,
    )

    element_lines: list[str] = []
    for node in sorted_nodes:
        role = role_map.get(str(node.get("id", "")))
        call = _node_to_dsl_call(node, semantic_role=role)
        if call:
            element_lines.append(call)

    if not element_lines:
        element_lines.append("    # No layout nodes found")

    lines = [
        "from __future__ import annotations",
        "",
        "from pathlib import Path",
        "",
        "from modu_math import Circle, Formula, Line, Polygon, Problem, Rect, Text",
        "from modu_math.renderer.svg.render import render_svg",
        "",
        f"# source semantic: {source_semantic_name}",
        f"# source layout: {source_layout_name}",
        f"# source renderer: {source_renderer_name}",
        "",
        f"PROBLEM_ID = {_py_literal(problem_id)}",
        f"PROBLEM_TYPE = {_py_literal(problem_type)}",
        f"RENDERER_JSON = {_py_literal(renderer_payload)}",
        "STRICT_DSL_SVG_ASSERT = False",
        "",
        "",
        "def build() -> Problem:",
        "    p = Problem(",
        f"        width=int({_py_literal(width)}),",
        f"        height=int({_py_literal(height)}),",
        f"        background={_py_literal(background)},",
        "        problem_id=PROBLEM_ID,",
        "        problem_type=PROBLEM_TYPE,",
        "    )",
        f"    p.set_metadata({_py_literal(metadata if isinstance(metadata, dict) else {})})",
        f"    p.set_domain({_py_literal(domain if isinstance(domain, dict) else {})})",
        "    p.set_answer(",
        f"        blanks={_py_literal(answer.get('blanks', []) if isinstance(answer, dict) else [])},",
        f"        choices={_py_literal(answer.get('choices', []) if isinstance(answer, dict) else [])},",
        f"        answer_key={_py_literal(answer.get('answer_key', []) if isinstance(answer, dict) else [])},",
        "    )",
        "",
        "    # Elements from layout.json (z-order sorted)",
    ]
    lines.extend(element_lines)
    lines.extend(
        [
            "",
            "    return p",
            "",
            "",
            "CURRENT_DIR = Path(__file__).resolve().parent",
            "",
            "def _first_diff_message(a: str, b: str) -> str:",
            "    n = min(len(a), len(b))",
            "    for i in range(n):",
            "        if a[i] != b[i]:",
            "            return f'first diff at index {i}: {a[i]!r} != {b[i]!r}'",
            "    return f'length mismatch: {len(a)} != {len(b)}'",
            "",
            "if __name__ == \"__main__\":",
            "    out_prefix = CURRENT_DIR / PROBLEM_ID",
            "    build().save(out_prefix)",
            "    dsl_svg_path = out_prefix.with_suffix('.svg')",
            "    dsl_svg = dsl_svg_path.read_text(encoding='utf-8')",
            "    renderer_svg = render_svg(RENDERER_JSON)",
            "    if STRICT_DSL_SVG_ASSERT:",
            "        assert dsl_svg == renderer_svg, 'DSL SVG mismatch with renderer SVG: ' + _first_diff_message(dsl_svg, renderer_svg)",
            "    # Keep final SVG identical to editor/renderer output.",
            "    dsl_svg_path.write_text(renderer_svg, encoding='utf-8')",
            "    final_svg = dsl_svg_path.read_text(encoding='utf-8')",
            "    assert final_svg == renderer_svg, 'Final SVG must match renderer SVG exactly'",
            "",
        ]
    )
    return "\n".join(lines)
