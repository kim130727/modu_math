from __future__ import annotations

import ast
from collections.abc import Mapping, Sequence
from pprint import pformat
from typing import Any

from .models.base import BlankSlot, Canvas, ChoiceSlot, CircleSlot, Constraint, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, Region, TextSlot
from .models.objects import Arrow, Circle, Cube, FractionAreaModel, Grid, ShapeObject, Triangle
from .models.templates import DiagramTemplate, ProblemTemplate


def problem_template_from_layout(
    layout: Mapping[str, Any],
    *,
    semantic: Mapping[str, Any] | None = None,
) -> ProblemTemplate:
    """Reconstruct a high-level DSL ProblemTemplate from normalized layout JSON."""
    problem_id = _require_non_empty_str(layout.get("problem_id"), "problem_id")
    title_raw = layout.get("title")
    title = title_raw if isinstance(title_raw, str) else ""

    canvas_raw = _require_mapping(layout.get("canvas"), "canvas")
    canvas = Canvas(
        width=int(_require_number(canvas_raw.get("width"), "canvas.width")),
        height=int(_require_number(canvas_raw.get("height"), "canvas.height")),
        coordinate_mode=_coordinate_mode(canvas_raw.get("coordinate_mode")),
    )

    regions = tuple(_region_from_layout(item, index) for index, item in enumerate(_sequence(layout.get("regions"))))
    choice_answer_keys, blank_answer_keys = _build_slot_answer_maps(semantic)
    slots = tuple(
        _slot_from_layout(
            item,
            index,
            choice_answer_keys=choice_answer_keys,
            blank_answer_keys=blank_answer_keys,
        )
        for index, item in enumerate(_sequence(layout.get("slots")))
    )
    groups = tuple(_group_from_layout(item, index) for index, item in enumerate(_sequence(layout.get("groups"))))
    constraints = tuple(
        _constraint_from_layout(item, index) for index, item in enumerate(_sequence(layout.get("constraints")))
    )
    diagrams = tuple(_diagram_from_layout(item, index) for index, item in enumerate(_sequence(layout.get("diagrams"))))

    return ProblemTemplate(
        id=problem_id,
        title=title,
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


def export_layout_to_dsl_source(
    layout: Mapping[str, Any],
    *,
    semantic: Mapping[str, Any] | None = None,
    function_name: str = "build_problem_template",
    variable_name: str = "PROBLEM_TEMPLATE",
) -> str:
    """Generate deterministic canonical Python DSL source code from normalized layout."""
    if not function_name.isidentifier():
        raise ValueError(f"function_name must be a valid identifier: {function_name!r}")
    if not variable_name.isidentifier():
        raise ValueError(f"variable_name must be a valid identifier: {variable_name!r}")

    template = problem_template_from_layout(layout, semantic=semantic)
    return _render_problem_template_source(template, function_name=function_name, variable_name=variable_name)


def _render_problem_template_source(
    template: ProblemTemplate,
    *,
    function_name: str,
    variable_name: str,
) -> str:
    lines: list[str] = [
        "from __future__ import annotations",
        "",
        "from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle",
        "",
        f"def {function_name}() -> ProblemTemplate:",
    ]

    lines.extend(_format_call_assignment("canvas", "Canvas", _canvas_kwargs(template.canvas), indent=1))
    lines.extend(_format_tuple_assignment("regions", [_region_kwargs(region) for region in template.regions], "Region", indent=1))
    lines.extend(_format_tuple_assignment("slots", [_slot_kwargs(slot) for slot in template.slots], None, indent=1))
    lines.extend(
        _format_tuple_assignment("diagrams", [_diagram_kwargs(diagram) for diagram in template.diagrams], None, indent=1)
    )
    lines.extend(_format_tuple_assignment("groups", [_group_kwargs(group) for group in template.groups], "Group", indent=1))
    lines.extend(
        _format_tuple_assignment(
            "constraints",
            [_constraint_kwargs(constraint) for constraint in template.constraints],
            "Constraint",
            indent=1,
        )
    )

    lines.extend(
        _format_call_lines(
            "ProblemTemplate",
            [
                ("id", template.id),
                ("title", template.title),
                ("canvas", "canvas"),
                ("regions", "regions"),
                ("slots", "slots"),
                ("diagrams", "diagrams"),
                ("groups", "groups"),
                ("constraints", "constraints"),
            ],
            indent=1,
            raw_keys={"canvas", "regions", "slots", "diagrams", "groups", "constraints"},
            assign_to="return",
            trailing_comma=False,
        )
    )
    lines.extend(["", f"{variable_name} = {function_name}()", ""])
    return "\n".join(lines)


def _format_call_assignment(name: str, ctor: str, kwargs: list[tuple[str, Any]], *, indent: int) -> list[str]:
    return _format_call_lines(ctor, kwargs, indent=indent, assign_to=name, trailing_comma=False)


def _format_tuple_assignment(
    name: str,
    items: list[list[tuple[str, Any]]],
    ctor: str | None,
    *,
    indent: int,
) -> list[str]:
    prefix = "    " * indent
    out = [f"{prefix}{name} = ("]
    if not items:
        out.append(f"{prefix})")
        return out
    for kwargs in items:
        if ctor:
            raw_keys = {"objects", "label_slots", "constraints"} if ctor == "DiagramTemplate" else None
            out.extend(_format_call_lines(ctor, kwargs, indent=indent + 1, raw_keys=raw_keys))
            continue
        item_ctor = _infer_ctor(kwargs)
        item_raw_keys = {"objects", "label_slots", "constraints"} if item_ctor == "DiagramTemplate" else None
        out.extend(_format_call_lines(item_ctor, kwargs, indent=indent + 1, raw_keys=item_raw_keys))
    out.append(f"{prefix})")
    return out


def _format_call_lines(
    ctor: str,
    kwargs: list[tuple[str, Any]],
    *,
    indent: int,
    assign_to: str | None = None,
    raw_keys: set[str] | None = None,
    trailing_comma: bool = True,
) -> list[str]:
    prefix = "    " * indent
    head = f"{ctor}("
    if assign_to == "return":
        out = [f"{prefix}return {head}"]
    elif assign_to:
        out = [f"{prefix}{assign_to} = {head}"]
    else:
        out = [f"{prefix}{head}"]

    for key, value in kwargs:
        if raw_keys and key in raw_keys:
            out.append(f"{prefix}    {key}={value},")
            continue
        lit = _format_literal(value)
        lit_lines = lit.splitlines()
        if len(lit_lines) == 1:
            out.append(f"{prefix}    {key}={lit_lines[0]},")
        else:
            out.append(f"{prefix}    {key}={lit_lines[0]}")
            for line in lit_lines[1:]:
                out.append(f"{prefix}    {line}")
            out[-1] = out[-1] + ","
    closing = f"{prefix})"
    if trailing_comma:
        closing += ","
    out.append(closing)
    return out


def _format_literal(value: Any) -> str:
    if isinstance(value, dict):
        value = dict(sorted(value.items(), key=lambda item: str(item[0])))
    return pformat(value, width=88, sort_dicts=True)


def _canvas_kwargs(canvas: Canvas) -> list[tuple[str, Any]]:
    return [
        ("width", canvas.width),
        ("height", canvas.height),
        ("coordinate_mode", canvas.coordinate_mode),
    ]


def _region_kwargs(region: Region) -> list[tuple[str, Any]]:
    return [
        ("id", region.id),
        ("role", region.role),
        ("flow", region.flow),
        ("slot_ids", tuple(region.slot_ids)),
    ]


def _slot_kwargs(slot: TextSlot | ChoiceSlot | BlankSlot | LabelSlot | RectSlot | LineSlot | CircleSlot | PolygonSlot | PathSlot) -> list[tuple[str, Any]]:
    if isinstance(slot, TextSlot):
        out: list[tuple[str, Any]] = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("text", slot.text),
            ("style_role", slot.style_role),
            ("__ctor__", "TextSlot"),
        ]
        if slot.x is not None:
            out.append(("x", slot.x))
        if slot.y is not None:
            out.append(("y", slot.y))
        if slot.font_size is not None:
            out.append(("font_size", slot.font_size))
        if isinstance(slot.font_family, str) and slot.font_family:
            out.append(("font_family", slot.font_family))
        if isinstance(slot.anchor, str) and slot.anchor:
            out.append(("anchor", slot.anchor))
        if isinstance(slot.fill, str) and slot.fill:
            out.append(("fill", slot.fill))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    if isinstance(slot, ChoiceSlot):
        out: list[tuple[str, Any]] = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("choices", tuple(slot.choices)),
            ("multiple_select", slot.multiple_select),
            ("__ctor__", "ChoiceSlot"),
        ]
        if slot.answer_key:
            out.append(("answer_key", tuple(slot.answer_key)))
        return out
    if isinstance(slot, BlankSlot):
        out = [("id", slot.id), ("prompt", slot.prompt), ("placeholder", slot.placeholder), ("__ctor__", "BlankSlot")]
        if slot.answer_key is not None:
            out.append(("answer_key", slot.answer_key))
        return out
    if isinstance(slot, RectSlot):
        out = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("x", slot.x),
            ("y", slot.y),
            ("width", slot.width),
            ("height", slot.height),
            ("__ctor__", "RectSlot"),
        ]
        if isinstance(slot.stroke, str):
            out.append(("stroke", slot.stroke))
        if slot.stroke_width is not None:
            out.append(("stroke_width", slot.stroke_width))
        if slot.rx is not None:
            out.append(("rx", slot.rx))
        if slot.ry is not None:
            out.append(("ry", slot.ry))
        if isinstance(slot.fill, str):
            out.append(("fill", slot.fill))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    if isinstance(slot, LineSlot):
        out = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("x1", slot.x1),
            ("y1", slot.y1),
            ("x2", slot.x2),
            ("y2", slot.y2),
            ("__ctor__", "LineSlot"),
        ]
        if isinstance(slot.stroke, str):
            out.append(("stroke", slot.stroke))
        if slot.stroke_width is not None:
            out.append(("stroke_width", slot.stroke_width))
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            out.append(("stroke_dasharray", slot.stroke_dasharray))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    if isinstance(slot, CircleSlot):
        out = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("cx", slot.cx),
            ("cy", slot.cy),
            ("r", slot.r),
            ("__ctor__", "CircleSlot"),
        ]
        if isinstance(slot.stroke, str):
            out.append(("stroke", slot.stroke))
        if slot.stroke_width is not None:
            out.append(("stroke_width", slot.stroke_width))
        if isinstance(slot.fill, str):
            out.append(("fill", slot.fill))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    if isinstance(slot, PolygonSlot):
        out = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("points", tuple((float(x), float(y)) for x, y in slot.points)),
            ("__ctor__", "PolygonSlot"),
        ]
        if isinstance(slot.stroke, str):
            out.append(("stroke", slot.stroke))
        if slot.stroke_width is not None:
            out.append(("stroke_width", slot.stroke_width))
        if isinstance(slot.fill, str):
            out.append(("fill", slot.fill))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    if isinstance(slot, PathSlot):
        out = [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("d", slot.d),
            ("__ctor__", "PathSlot"),
        ]
        if isinstance(slot.stroke, str):
            out.append(("stroke", slot.stroke))
        if slot.stroke_width is not None:
            out.append(("stroke_width", slot.stroke_width))
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            out.append(("stroke_dasharray", slot.stroke_dasharray))
        if isinstance(slot.fill, str):
            out.append(("fill", slot.fill))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            out.append(("semantic_role", slot.semantic_role))
        return out
    return [
        ("id", slot.id),
        ("prompt", slot.prompt),
        ("text", slot.text),
        ("target_object_id", slot.target_object_id),
        ("target_anchor", slot.target_anchor),
        ("__ctor__", "LabelSlot"),
    ]


def _group_kwargs(group: Group) -> list[tuple[str, Any]]:
    return [
        ("id", group.id),
        ("member_ids", tuple(group.member_ids)),
        ("role", group.role),
    ]


def _constraint_kwargs(constraint: Constraint) -> list[tuple[str, Any]]:
    return [
        ("id", constraint.id),
        ("type", constraint.type),
        ("target_ids", tuple(constraint.target_ids)),
        ("params", dict(sorted(constraint.params.items(), key=lambda item: item[0]))),
    ]


def _diagram_kwargs(diagram: DiagramTemplate) -> list[tuple[str, Any]]:
    return [
        ("id", diagram.id),
        ("objects", _tuple_expr_repr([_shape_call_repr(shape) for shape in diagram.objects])),
        ("label_slots", _tuple_expr_repr([_slot_call_repr(slot) for slot in diagram.label_slots])),
        ("constraints", _tuple_expr_repr([_constraint_call_repr(item) for item in diagram.constraints])),
        ("__ctor__", "DiagramTemplate"),
    ]


def _shape_call_repr(shape: ShapeObject) -> str:
    if isinstance(shape, Cube):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("edge_label_mode", shape.edge_label_mode), ("perspective", shape.perspective)]
        return _call_repr("Cube", kwargs)
    if isinstance(shape, Triangle):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("variant", shape.variant)]
        return _call_repr("Triangle", kwargs)
    if isinstance(shape, Circle):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("mark_center", shape.mark_center)]
        return _call_repr("Circle", kwargs)
    if isinstance(shape, Grid):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("rows", shape.rows), ("cols", shape.cols)]
        return _call_repr("Grid", kwargs)
    if isinstance(shape, Arrow):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("direction", shape.direction)]
        return _call_repr("Arrow", kwargs)
    if isinstance(shape, FractionAreaModel):
        kwargs = [("id", shape.id), ("style_role", shape.style_role), ("partitions", shape.partitions), ("shaded", shape.shaded), ("orientation", shape.orientation)]
        return _call_repr("FractionAreaModel", kwargs)
    kwargs = [("id", shape.id), ("object_type", shape.object_type), ("style_role", shape.style_role)]
    return _call_repr("ShapeObject", kwargs)


def _slot_call_repr(slot: LabelSlot) -> str:
    return _call_repr(
        "LabelSlot",
        [
            ("id", slot.id),
            ("prompt", slot.prompt),
            ("text", slot.text),
            ("target_object_id", slot.target_object_id),
            ("target_anchor", slot.target_anchor),
        ],
    )


def _constraint_call_repr(constraint: Constraint) -> str:
    return _call_repr(
        "Constraint",
        [
            ("id", constraint.id),
            ("type", constraint.type),
            ("target_ids", tuple(constraint.target_ids)),
            ("params", dict(sorted(constraint.params.items(), key=lambda item: item[0]))),
        ],
    )


def _call_repr(ctor: str, kwargs: list[tuple[str, Any]]) -> str:
    joined = ", ".join(f"{key}={_format_literal(value)}" for key, value in kwargs)
    return f"{ctor}({joined})"


def _tuple_expr_repr(items: list[str]) -> str:
    if not items:
        return "()"
    if len(items) == 1:
        return f"({items[0]},)"
    return f"({', '.join(items)})"


def _infer_ctor(kwargs: list[tuple[str, Any]]) -> str:
    ctor = "TextSlot"
    filtered: list[tuple[str, Any]] = []
    for key, value in kwargs:
        if key == "__ctor__":
            ctor = str(value)
            continue
        filtered.append((key, value))
    kwargs[:] = filtered
    return ctor


def _problem_template_expr(template: ProblemTemplate) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="ProblemTemplate", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=template.id)),
            ast.keyword(arg="title", value=ast.Constant(value=template.title)),
            ast.keyword(arg="canvas", value=_canvas_expr(template.canvas)),
            ast.keyword(arg="regions", value=_tuple_expr(_region_expr(region) for region in template.regions)),
            ast.keyword(arg="slots", value=_tuple_expr(_slot_expr(slot) for slot in template.slots)),
            ast.keyword(arg="diagrams", value=_tuple_expr(_diagram_expr(diagram) for diagram in template.diagrams)),
            ast.keyword(arg="groups", value=_tuple_expr(_group_expr(group) for group in template.groups)),
            ast.keyword(
                arg="constraints",
                value=_tuple_expr(_constraint_expr(constraint) for constraint in template.constraints),
            ),
        ],
    )


def _canvas_expr(canvas: Canvas) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="Canvas", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="width", value=ast.Constant(value=canvas.width)),
            ast.keyword(arg="height", value=ast.Constant(value=canvas.height)),
            ast.keyword(arg="coordinate_mode", value=ast.Constant(value=canvas.coordinate_mode)),
        ],
    )


def _region_expr(region: Region) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="Region", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=region.id)),
            ast.keyword(arg="role", value=ast.Constant(value=region.role)),
            ast.keyword(arg="flow", value=ast.Constant(value=region.flow)),
            ast.keyword(arg="slot_ids", value=_tuple_expr(ast.Constant(value=item) for item in region.slot_ids)),
        ],
    )


def _slot_expr(slot: TextSlot | ChoiceSlot | BlankSlot | LabelSlot | RectSlot | LineSlot | CircleSlot | PolygonSlot | PathSlot) -> ast.expr:
    if isinstance(slot, TextSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="text", value=ast.Constant(value=slot.text)),
            ast.keyword(arg="style_role", value=ast.Constant(value=slot.style_role)),
        ]
        if slot.x is not None:
            keywords.append(ast.keyword(arg="x", value=ast.Constant(value=slot.x)))
        if slot.y is not None:
            keywords.append(ast.keyword(arg="y", value=ast.Constant(value=slot.y)))
        if slot.font_size is not None:
            keywords.append(ast.keyword(arg="font_size", value=ast.Constant(value=slot.font_size)))
        if isinstance(slot.font_family, str) and slot.font_family:
            keywords.append(ast.keyword(arg="font_family", value=ast.Constant(value=slot.font_family)))
        if isinstance(slot.anchor, str) and slot.anchor:
            keywords.append(ast.keyword(arg="anchor", value=ast.Constant(value=slot.anchor)))
        if isinstance(slot.fill, str) and slot.fill:
            keywords.append(ast.keyword(arg="fill", value=ast.Constant(value=slot.fill)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(
            func=ast.Name(id="TextSlot", ctx=ast.Load()),
            args=[],
            keywords=keywords,
        )
    if isinstance(slot, ChoiceSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="choices", value=_tuple_expr(ast.Constant(value=item) for item in slot.choices)),
            ast.keyword(arg="multiple_select", value=ast.Constant(value=slot.multiple_select)),
        ]
        if slot.answer_key:
            keywords.append(ast.keyword(arg="answer_key", value=_tuple_expr(ast.Constant(value=item) for item in slot.answer_key)))
        return ast.Call(
            func=ast.Name(id="ChoiceSlot", ctx=ast.Load()),
            args=[],
            keywords=keywords,
        )
    if isinstance(slot, BlankSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="placeholder", value=ast.Constant(value=slot.placeholder)),
        ]
        if slot.answer_key is not None:
            keywords.append(ast.keyword(arg="answer_key", value=ast.Constant(value=slot.answer_key)))
        return ast.Call(
            func=ast.Name(id="BlankSlot", ctx=ast.Load()),
            args=[],
            keywords=keywords,
        )
    if isinstance(slot, RectSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="x", value=ast.Constant(value=slot.x)),
            ast.keyword(arg="y", value=ast.Constant(value=slot.y)),
            ast.keyword(arg="width", value=ast.Constant(value=slot.width)),
            ast.keyword(arg="height", value=ast.Constant(value=slot.height)),
        ]
        if isinstance(slot.stroke, str):
            keywords.append(ast.keyword(arg="stroke", value=ast.Constant(value=slot.stroke)))
        if slot.stroke_width is not None:
            keywords.append(ast.keyword(arg="stroke_width", value=ast.Constant(value=slot.stroke_width)))
        if slot.rx is not None:
            keywords.append(ast.keyword(arg="rx", value=ast.Constant(value=slot.rx)))
        if slot.ry is not None:
            keywords.append(ast.keyword(arg="ry", value=ast.Constant(value=slot.ry)))
        if isinstance(slot.fill, str):
            keywords.append(ast.keyword(arg="fill", value=ast.Constant(value=slot.fill)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(func=ast.Name(id="RectSlot", ctx=ast.Load()), args=[], keywords=keywords)
    if isinstance(slot, LineSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="x1", value=ast.Constant(value=slot.x1)),
            ast.keyword(arg="y1", value=ast.Constant(value=slot.y1)),
            ast.keyword(arg="x2", value=ast.Constant(value=slot.x2)),
            ast.keyword(arg="y2", value=ast.Constant(value=slot.y2)),
        ]
        if isinstance(slot.stroke, str):
            keywords.append(ast.keyword(arg="stroke", value=ast.Constant(value=slot.stroke)))
        if slot.stroke_width is not None:
            keywords.append(ast.keyword(arg="stroke_width", value=ast.Constant(value=slot.stroke_width)))
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            keywords.append(ast.keyword(arg="stroke_dasharray", value=ast.Constant(value=slot.stroke_dasharray)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(func=ast.Name(id="LineSlot", ctx=ast.Load()), args=[], keywords=keywords)
    if isinstance(slot, CircleSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="cx", value=ast.Constant(value=slot.cx)),
            ast.keyword(arg="cy", value=ast.Constant(value=slot.cy)),
            ast.keyword(arg="r", value=ast.Constant(value=slot.r)),
        ]
        if isinstance(slot.stroke, str):
            keywords.append(ast.keyword(arg="stroke", value=ast.Constant(value=slot.stroke)))
        if slot.stroke_width is not None:
            keywords.append(ast.keyword(arg="stroke_width", value=ast.Constant(value=slot.stroke_width)))
        if isinstance(slot.fill, str):
            keywords.append(ast.keyword(arg="fill", value=ast.Constant(value=slot.fill)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(func=ast.Name(id="CircleSlot", ctx=ast.Load()), args=[], keywords=keywords)
    if isinstance(slot, PolygonSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(
                arg="points",
                value=_tuple_expr(
                    ast.Tuple(elts=[ast.Constant(value=float(x)), ast.Constant(value=float(y))], ctx=ast.Load())
                    for x, y in slot.points
                ),
            ),
        ]
        if isinstance(slot.stroke, str):
            keywords.append(ast.keyword(arg="stroke", value=ast.Constant(value=slot.stroke)))
        if slot.stroke_width is not None:
            keywords.append(ast.keyword(arg="stroke_width", value=ast.Constant(value=slot.stroke_width)))
        if isinstance(slot.fill, str):
            keywords.append(ast.keyword(arg="fill", value=ast.Constant(value=slot.fill)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(func=ast.Name(id="PolygonSlot", ctx=ast.Load()), args=[], keywords=keywords)
    if isinstance(slot, PathSlot):
        keywords = [
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="d", value=ast.Constant(value=slot.d)),
        ]
        if isinstance(slot.stroke, str):
            keywords.append(ast.keyword(arg="stroke", value=ast.Constant(value=slot.stroke)))
        if slot.stroke_width is not None:
            keywords.append(ast.keyword(arg="stroke_width", value=ast.Constant(value=slot.stroke_width)))
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            keywords.append(ast.keyword(arg="stroke_dasharray", value=ast.Constant(value=slot.stroke_dasharray)))
        if isinstance(slot.fill, str):
            keywords.append(ast.keyword(arg="fill", value=ast.Constant(value=slot.fill)))
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            keywords.append(ast.keyword(arg="semantic_role", value=ast.Constant(value=slot.semantic_role)))
        return ast.Call(func=ast.Name(id="PathSlot", ctx=ast.Load()), args=[], keywords=keywords)
    return ast.Call(
        func=ast.Name(id="LabelSlot", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=slot.id)),
            ast.keyword(arg="prompt", value=ast.Constant(value=slot.prompt)),
            ast.keyword(arg="text", value=ast.Constant(value=slot.text)),
            ast.keyword(arg="target_object_id", value=ast.Constant(value=slot.target_object_id)),
            ast.keyword(arg="target_anchor", value=ast.Constant(value=slot.target_anchor)),
        ],
    )


def _group_expr(group: Group) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="Group", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=group.id)),
            ast.keyword(arg="member_ids", value=_tuple_expr(ast.Constant(value=item) for item in group.member_ids)),
            ast.keyword(arg="role", value=ast.Constant(value=group.role)),
        ],
    )


def _constraint_expr(constraint: Constraint) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="Constraint", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=constraint.id)),
            ast.keyword(arg="type", value=ast.Constant(value=constraint.type)),
            ast.keyword(arg="target_ids", value=_tuple_expr(ast.Constant(value=item) for item in constraint.target_ids)),
            ast.keyword(arg="params", value=_dict_expr(constraint.params)),
        ],
    )


def _diagram_expr(diagram: DiagramTemplate) -> ast.expr:
    return ast.Call(
        func=ast.Name(id="DiagramTemplate", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=diagram.id)),
            ast.keyword(arg="objects", value=_tuple_expr(_shape_expr(item) for item in diagram.objects)),
            ast.keyword(arg="label_slots", value=_tuple_expr(_slot_expr(item) for item in diagram.label_slots)),
            ast.keyword(arg="constraints", value=_tuple_expr(_constraint_expr(item) for item in diagram.constraints)),
        ],
    )


def _shape_expr(shape: ShapeObject) -> ast.expr:
    if isinstance(shape, Cube):
        return ast.Call(
            func=ast.Name(id="Cube", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="edge_label_mode", value=ast.Constant(value=shape.edge_label_mode)),
                ast.keyword(arg="perspective", value=ast.Constant(value=shape.perspective)),
            ],
        )
    if isinstance(shape, Triangle):
        return ast.Call(
            func=ast.Name(id="Triangle", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="variant", value=ast.Constant(value=shape.variant)),
            ],
        )
    if isinstance(shape, Circle):
        return ast.Call(
            func=ast.Name(id="Circle", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="mark_center", value=ast.Constant(value=shape.mark_center)),
            ],
        )
    if isinstance(shape, Grid):
        return ast.Call(
            func=ast.Name(id="Grid", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="rows", value=ast.Constant(value=shape.rows)),
                ast.keyword(arg="cols", value=ast.Constant(value=shape.cols)),
            ],
        )
    if isinstance(shape, Arrow):
        return ast.Call(
            func=ast.Name(id="Arrow", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="direction", value=ast.Constant(value=shape.direction)),
            ],
        )
    if isinstance(shape, FractionAreaModel):
        return ast.Call(
            func=ast.Name(id="FractionAreaModel", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
                ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
                ast.keyword(arg="partitions", value=ast.Constant(value=shape.partitions)),
                ast.keyword(arg="shaded", value=ast.Constant(value=shape.shaded)),
                ast.keyword(arg="orientation", value=ast.Constant(value=shape.orientation)),
            ],
        )
    return ast.Call(
        func=ast.Name(id="ShapeObject", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="id", value=ast.Constant(value=shape.id)),
            ast.keyword(arg="object_type", value=ast.Constant(value=shape.object_type)),
            ast.keyword(arg="style_role", value=ast.Constant(value=shape.style_role)),
        ],
    )


def _tuple_expr(values: Sequence[ast.expr] | Any) -> ast.expr:
    return ast.Tuple(elts=list(values), ctx=ast.Load())


def _dict_expr(data: Mapping[str, Any]) -> ast.expr:
    ordered_items = sorted(data.items(), key=lambda item: item[0])
    return ast.Dict(
        keys=[ast.Constant(value=key) for key, _ in ordered_items],
        values=[_literal_expr(value) for _, value in ordered_items],
    )


def _literal_expr(value: Any) -> ast.expr:
    if isinstance(value, dict):
        ordered = sorted(value.items(), key=lambda item: str(item[0]))
        return ast.Dict(
            keys=[_literal_expr(key) for key, _ in ordered],
            values=[_literal_expr(item_value) for _, item_value in ordered],
        )
    if isinstance(value, list):
        return ast.List(elts=[_literal_expr(item) for item in value], ctx=ast.Load())
    if isinstance(value, tuple):
        return ast.Tuple(elts=[_literal_expr(item) for item in value], ctx=ast.Load())
    if isinstance(value, (str, int, float, bool)) or value is None:
        return ast.Constant(value=value)
    raise TypeError(f"Unsupported literal type in constraint params: {type(value)!r}")


def _region_from_layout(raw: Any, index: int) -> Region:
    data = _require_mapping(raw, f"regions[{index}]")
    return Region(
        id=_require_non_empty_str(data.get("id"), f"regions[{index}].id"),
        role=_region_role(data.get("role")),
        flow=_region_flow(data.get("flow")),
        slot_ids=tuple(_string_list(data.get("slot_ids"), f"regions[{index}].slot_ids")),
    )


def _slot_from_layout(
    raw: Any,
    index: int,
    *,
    choice_answer_keys: Mapping[str, tuple[str, ...]] | None = None,
    blank_answer_keys: Mapping[str, str] | None = None,
) -> TextSlot | ChoiceSlot | BlankSlot | LabelSlot | RectSlot | LineSlot | CircleSlot | PolygonSlot | PathSlot:
    data = _require_mapping(raw, f"slots[{index}]")
    slot_id = _require_non_empty_str(data.get("id"), f"slots[{index}].id")
    kind = _require_non_empty_str(data.get("kind"), f"slots[{index}].kind")
    prompt_raw = data.get("prompt")
    prompt = prompt_raw if isinstance(prompt_raw, str) else None
    content = _require_mapping(data.get("content"), f"slots[{index}].content")

    if kind == "text":
        return TextSlot(
            id=slot_id,
            prompt=prompt,
            text=_string(content.get("text"), ""),
            style_role=_string(content.get("style_role"), "body"),
            x=_number_or_none(content.get("x")),
            y=_number_or_none(content.get("y")),
            font_size=_int_or_none(content.get("font_size")),
            font_family=_string(content.get("font_family"), None),
            anchor=_string(content.get("anchor"), None),
            fill=_string(content.get("fill"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    if kind == "choice":
        choice_answer_key = _lookup_choice_answer_key(choice_answer_keys, slot_id)
        return ChoiceSlot(
            id=slot_id,
            prompt=prompt,
            choices=tuple(_string_list(content.get("choices"), f"slots[{index}].content.choices")),
            answer_key=choice_answer_key,
            multiple_select=bool(content.get("multiple_select", False)),
        )
    if kind == "blank":
        blank_answer_key = _lookup_blank_answer_key(blank_answer_keys, slot_id)
        return BlankSlot(
            id=slot_id,
            prompt=prompt,
            placeholder=_string(content.get("placeholder"), ""),
            answer_key=blank_answer_key,
        )
    if kind == "label":
        return LabelSlot(
            id=slot_id,
            prompt=prompt,
            text=_string(content.get("text"), ""),
            target_object_id=_string(content.get("target_object_id"), ""),
            target_anchor=_label_anchor(content.get("target_anchor")),
        )
    if kind == "rect":
        return RectSlot(
            id=slot_id,
            prompt=prompt,
            x=float(_require_number(content.get("x"), f"slots[{index}].content.x")),
            y=float(_require_number(content.get("y"), f"slots[{index}].content.y")),
            width=float(_require_number(content.get("width"), f"slots[{index}].content.width")),
            height=float(_require_number(content.get("height"), f"slots[{index}].content.height")),
            stroke=_string(content.get("stroke"), None),
            stroke_width=_number_or_none(content.get("stroke_width")),
            rx=_number_or_none(content.get("rx")),
            ry=_number_or_none(content.get("ry")),
            fill=_string(content.get("fill"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    if kind == "line":
        return LineSlot(
            id=slot_id,
            prompt=prompt,
            x1=float(_require_number(content.get("x1"), f"slots[{index}].content.x1")),
            y1=float(_require_number(content.get("y1"), f"slots[{index}].content.y1")),
            x2=float(_require_number(content.get("x2"), f"slots[{index}].content.x2")),
            y2=float(_require_number(content.get("y2"), f"slots[{index}].content.y2")),
            stroke=_string(content.get("stroke"), None),
            stroke_width=_number_or_none(content.get("stroke_width")),
            stroke_dasharray=_string(content.get("stroke_dasharray"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    if kind == "circle":
        return CircleSlot(
            id=slot_id,
            prompt=prompt,
            cx=float(_require_number(content.get("cx"), f"slots[{index}].content.cx")),
            cy=float(_require_number(content.get("cy"), f"slots[{index}].content.cy")),
            r=float(_require_number(content.get("r"), f"slots[{index}].content.r")),
            stroke=_string(content.get("stroke"), None),
            stroke_width=_number_or_none(content.get("stroke_width")),
            fill=_string(content.get("fill"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    if kind == "polygon":
        points_raw = content.get("points")
        points: list[tuple[float, float]] = []
        if isinstance(points_raw, list):
            for point in points_raw:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    points.append((float(_as_float(point[0], 0.0)), float(_as_float(point[1], 0.0))))
        return PolygonSlot(
            id=slot_id,
            prompt=prompt,
            points=tuple(points),
            stroke=_string(content.get("stroke"), None),
            stroke_width=_number_or_none(content.get("stroke_width")),
            fill=_string(content.get("fill"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    if kind == "path":
        return PathSlot(
            id=slot_id,
            prompt=prompt,
            d=_string(content.get("d"), "") or "",
            stroke=_string(content.get("stroke"), None),
            stroke_width=_number_or_none(content.get("stroke_width")),
            stroke_dasharray=_string(content.get("stroke_dasharray"), None),
            fill=_string(content.get("fill"), None),
            semantic_role=_string(content.get("semantic_role"), None),
        )
    raise ValueError(f"Unsupported slot kind: {kind!r}")


def _group_from_layout(raw: Any, index: int) -> Group:
    data = _require_mapping(raw, f"groups[{index}]")
    return Group(
        id=_require_non_empty_str(data.get("id"), f"groups[{index}].id"),
        member_ids=tuple(_string_list(data.get("member_ids"), f"groups[{index}].member_ids")),
        role=_group_role(data.get("role")),
    )


def _constraint_from_layout(raw: Any, index: int) -> Constraint:
    data = _require_mapping(raw, f"constraints[{index}]")
    params_raw = data.get("params")
    params = _string_key_dict(params_raw, f"constraints[{index}].params")
    return Constraint(
        id=_require_non_empty_str(data.get("id"), f"constraints[{index}].id"),
        type=_constraint_type(data.get("type")),
        target_ids=tuple(_string_list(data.get("target_ids"), f"constraints[{index}].target_ids")),
        params=params,
    )


def _diagram_from_layout(raw: Any, index: int) -> DiagramTemplate:
    data = _require_mapping(raw, f"diagrams[{index}]")
    objects = tuple(
        _shape_from_layout(item, index, object_index)
        for object_index, item in enumerate(_sequence(data.get("objects")))
    )
    label_slots = tuple(
        _label_slot_from_layout(item, index, label_index)
        for label_index, item in enumerate(_sequence(data.get("label_slots")))
    )
    constraints = tuple(
        _constraint_from_layout(item, constraint_index)
        for constraint_index, item in enumerate(_sequence(data.get("constraints")))
    )
    return DiagramTemplate(
        id=_require_non_empty_str(data.get("id"), f"diagrams[{index}].id"),
        objects=objects,
        label_slots=label_slots,
        constraints=constraints,
    )


def _shape_from_layout(raw: Any, diagram_index: int, object_index: int) -> ShapeObject:
    path = f"diagrams[{diagram_index}].objects[{object_index}]"
    data = _require_mapping(raw, path)
    object_id = _require_non_empty_str(data.get("id"), f"{path}.id")
    object_type = _require_non_empty_str(data.get("object_type"), f"{path}.object_type")
    style_role = _string(data.get("style_role"), "default")

    if object_type == "cube":
        return Cube(
            id=object_id,
            style_role=style_role,
            edge_label_mode=_cube_edge_label_mode(data.get("edge_label_mode")),
            perspective=_cube_perspective(data.get("perspective")),
        )
    if object_type == "triangle":
        return Triangle(
            id=object_id,
            style_role=style_role,
            variant=_triangle_variant(data.get("variant")),
        )
    if object_type == "circle":
        return Circle(
            id=object_id,
            style_role=style_role,
            mark_center=bool(data.get("mark_center", False)),
        )
    if object_type == "grid":
        return Grid(
            id=object_id,
            style_role=style_role,
            rows=int(_require_number(data.get("rows"), f"{path}.rows")),
            cols=int(_require_number(data.get("cols"), f"{path}.cols")),
        )
    if object_type == "arrow":
        return Arrow(
            id=object_id,
            style_role=style_role,
            direction=_arrow_direction(data.get("direction")),
        )
    if object_type == "fraction_area_model":
        return FractionAreaModel(
            id=object_id,
            style_role=style_role,
            partitions=int(_require_number(data.get("partitions"), f"{path}.partitions")),
            shaded=int(_require_number(data.get("shaded"), f"{path}.shaded")),
            orientation=_fraction_orientation(data.get("orientation")),
        )

    return ShapeObject(id=object_id, object_type=object_type, style_role=style_role)


def _label_slot_from_layout(raw: Any, diagram_index: int, slot_index: int) -> LabelSlot:
    data = _require_mapping(raw, f"diagrams[{diagram_index}].label_slots[{slot_index}]")
    if _string(data.get("kind"), "") not in {"", "label"}:
        raise ValueError(f"Diagram label slot must have kind='label' when provided: {data!r}")
    content = _require_mapping(data.get("content"), f"diagrams[{diagram_index}].label_slots[{slot_index}].content")
    return LabelSlot(
        id=_require_non_empty_str(data.get("id"), f"diagrams[{diagram_index}].label_slots[{slot_index}].id"),
        prompt=_string(data.get("prompt"), None),
        text=_string(content.get("text"), ""),
        target_object_id=_string(content.get("target_object_id"), ""),
        target_anchor=_label_anchor(content.get("target_anchor")),
    )


def _build_slot_answer_maps(
    semantic: Mapping[str, Any] | None,
) -> tuple[dict[str, tuple[str, ...]], dict[str, str]]:
    choice_answer_keys: dict[str, tuple[str, ...]] = {}
    blank_answer_keys: dict[str, str] = {}
    if not isinstance(semantic, Mapping):
        return choice_answer_keys, blank_answer_keys

    answer = semantic.get("answer")
    if not isinstance(answer, Mapping):
        return choice_answer_keys, blank_answer_keys

    answer_key_items = answer.get("answer_key")
    if isinstance(answer_key_items, list):
        for item in answer_key_items:
            if not isinstance(item, Mapping):
                continue
            slot_refs = [
                _string(item.get("slot_id"), None),
                _string(item.get("target"), None),
                _string(item.get("blank_id"), None),
            ]
            refs = [ref for ref in slot_refs if isinstance(ref, str) and ref]
            if not refs:
                continue

            values = item.get("values")
            if isinstance(values, list):
                tuple_values = tuple(str(value) for value in values if value is not None)
                if tuple_values:
                    for ref in refs:
                        choice_answer_keys[ref] = tuple_values

            value = item.get("value")
            if value is not None:
                rendered_value = str(value)
                for ref in refs:
                    blank_answer_keys[ref] = rendered_value

    blanks = answer.get("blanks")
    if isinstance(blanks, list):
        for blank in blanks:
            if not isinstance(blank, Mapping):
                continue
            slot_ref = _string(blank.get("slot_id"), None) or _string(blank.get("id"), None)
            expected = blank.get("expected")
            if slot_ref and expected is not None and slot_ref not in blank_answer_keys:
                blank_answer_keys[slot_ref] = str(expected)

    return choice_answer_keys, blank_answer_keys


def _lookup_choice_answer_key(
    answer_keys: Mapping[str, tuple[str, ...]] | None,
    slot_id: str,
) -> tuple[str, ...]:
    if not isinstance(answer_keys, Mapping):
        return ()
    for candidate in _candidate_slot_ids(slot_id):
        values = answer_keys.get(candidate)
        if isinstance(values, tuple):
            return values
    return ()


def _lookup_blank_answer_key(
    answer_keys: Mapping[str, str] | None,
    slot_id: str,
) -> str | None:
    if not isinstance(answer_keys, Mapping):
        return None
    for candidate in _candidate_slot_ids(slot_id):
        value = answer_keys.get(candidate)
        if isinstance(value, str):
            return value
    return None


def _candidate_slot_ids(slot_id: str) -> tuple[str, ...]:
    candidates = [slot_id]
    if slot_id.startswith("slot."):
        stripped = slot_id.removeprefix("slot.")
        if stripped:
            candidates.append(stripped)
    else:
        candidates.append(f"slot.{slot_id}")
    return tuple(candidates)


def _sequence(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    raise ValueError(f"Expected list, got {type(value)!r}")


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _require_number(value: Any, field_name: str) -> float:
    if not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number")
    return float(value)


def _number_or_none(value: Any) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    return None


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, int | float):
        return int(value)
    return None


def _as_float(value: Any, default: float) -> float:
    if isinstance(value, int | float):
        return float(value)
    return float(default)


def _string(value: Any, default: str | None) -> str | None:
    if isinstance(value, str):
        return value
    return default


def _string_list(value: Any, field_name: str) -> list[str]:
    data = _sequence(value)
    out: list[str] = []
    for index, item in enumerate(data):
        if not isinstance(item, str):
            raise ValueError(f"{field_name}[{index}] must be a string")
        out.append(item)
    return out


def _string_key_dict(value: Any, field_name: str) -> dict[str, str]:
    if value is None:
        return {}
    data = _require_mapping(value, field_name)
    out: dict[str, str] = {}
    for key, item in sorted(data.items(), key=lambda pair: str(pair[0])):
        if not isinstance(key, str):
            raise ValueError(f"{field_name} keys must be strings")
        if not isinstance(item, str):
            raise ValueError(f"{field_name}.{key} must be a string")
        out[key] = item
    return out


def _coordinate_mode(value: Any) -> str:
    mode = _string(value, "logical")
    if mode not in {"logical", "absolute"}:
        raise ValueError(f"Unsupported coordinate_mode: {mode!r}")
    return mode


def _region_role(value: Any) -> str:
    role = _string(value, "custom")
    allowed = {"stem", "diagram", "choices", "answer", "note", "custom"}
    if role not in allowed:
        raise ValueError(f"Unsupported region role: {role!r}")
    return role


def _region_flow(value: Any) -> str:
    flow = _string(value, "vertical")
    allowed = {"vertical", "horizontal", "absolute", "grid"}
    if flow not in allowed:
        raise ValueError(f"Unsupported region flow: {flow!r}")
    return flow


def _group_role(value: Any) -> str:
    role = _string(value, "custom")
    allowed = {"question_block", "diagram_block", "answer_block", "custom"}
    if role not in allowed:
        raise ValueError(f"Unsupported group role: {role!r}")
    return role


def _constraint_type(value: Any) -> str:
    constraint_type = _string(value, "align")
    allowed = {"align", "equal_size", "inside", "connect", "distribute"}
    if constraint_type not in allowed:
        raise ValueError(f"Unsupported constraint type: {constraint_type!r}")
    return constraint_type


def _label_anchor(value: Any) -> str:
    anchor = _string(value, "center")
    allowed = {"top", "right", "bottom", "left", "center"}
    if anchor not in allowed:
        raise ValueError(f"Unsupported label anchor: {anchor!r}")
    return anchor


def _cube_edge_label_mode(value: Any) -> str:
    edge_label_mode = _string(value, "none")
    allowed = {"none", "auto", "custom"}
    if edge_label_mode not in allowed:
        raise ValueError(f"Unsupported cube.edge_label_mode: {edge_label_mode!r}")
    return edge_label_mode


def _cube_perspective(value: Any) -> str:
    perspective = _string(value, "isometric")
    allowed = {"isometric", "cabinet"}
    if perspective not in allowed:
        raise ValueError(f"Unsupported cube.perspective: {perspective!r}")
    return perspective


def _triangle_variant(value: Any) -> str:
    variant = _string(value, "scalene")
    allowed = {"scalene", "isosceles", "equilateral", "right"}
    if variant not in allowed:
        raise ValueError(f"Unsupported triangle.variant: {variant!r}")
    return variant


def _arrow_direction(value: Any) -> str:
    direction = _string(value, "right")
    allowed = {"up", "right", "down", "left"}
    if direction not in allowed:
        raise ValueError(f"Unsupported arrow.direction: {direction!r}")
    return direction


def _fraction_orientation(value: Any) -> str:
    orientation = _string(value, "horizontal")
    allowed = {"horizontal", "vertical"}
    if orientation not in allowed:
        raise ValueError(f"Unsupported fraction_area_model.orientation: {orientation!r}")
    return orientation
