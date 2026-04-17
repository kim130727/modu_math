from __future__ import annotations

from html import escape

from .ir import Circle, Element, Formula, Line, Polygon, ProblemIR, Rect, Text


def _float_str(value: float) -> str:
    ivalue = int(value)
    return str(ivalue) if value == ivalue else str(value)


def _attrs_to_str(attrs: dict[str, str | None]) -> str:
    parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        parts.append(f'{key}="{escape(str(value), quote=True)}"')
    return " ".join(parts)


def _style_attrs(element: Element) -> dict[str, str | None]:
    attrs: dict[str, str | None] = {}
    if element.stroke is not None:
        attrs["stroke"] = element.stroke
    if element.stroke_width is not None:
        attrs["stroke-width"] = _float_str(float(element.stroke_width))
    if element.fill is not None:
        attrs["fill"] = element.fill
    if element.font_family is not None:
        attrs["font-family"] = element.font_family
    if element.font_size is not None:
        attrs["font-size"] = f"{_float_str(float(element.font_size))}px"
    if element.font_weight is not None:
        attrs["font-weight"] = element.font_weight
    return attrs


def _base_attrs(element: Element) -> dict[str, str | None]:
    attrs: dict[str, str | None] = {"id": element.id}
    if element.group is not None:
        attrs["data-group"] = element.group
    if element.semantic_role is not None:
        attrs["data-semantic-role"] = element.semantic_role
    attrs.update(_style_attrs(element))
    return attrs


def _element_to_svg_line(element: Element) -> str:
    attrs = _base_attrs(element)

    if isinstance(element, Rect):
        attrs.update(
            {
                "x": _float_str(float(element.x)),
                "y": _float_str(float(element.y)),
                "width": _float_str(float(element.width)),
                "height": _float_str(float(element.height)),
                "rx": _float_str(float(element.rx)) if element.rx is not None else None,
                "ry": _float_str(float(element.ry)) if element.ry is not None else None,
            }
        )
        return f"  <rect {_attrs_to_str(attrs)} />"

    if isinstance(element, Circle):
        attrs.update(
            {
                "cx": _float_str(float(element.x)),
                "cy": _float_str(float(element.y)),
                "r": _float_str(float(element.r)),
            }
        )
        return f"  <circle {_attrs_to_str(attrs)} />"

    if isinstance(element, Line):
        attrs.update(
            {
                "x1": _float_str(float(element.x1)),
                "y1": _float_str(float(element.y1)),
                "x2": _float_str(float(element.x2)),
                "y2": _float_str(float(element.y2)),
            }
        )
        return f"  <line {_attrs_to_str(attrs)} />"

    if isinstance(element, Polygon):
        points = " ".join([f"{_float_str(float(x))},{_float_str(float(y))}" for x, y in element.points])
        attrs.update({"points": points})
        return f"  <polygon {_attrs_to_str(attrs)} />"

    if isinstance(element, Text):
        attrs.update(
            {
                "x": _float_str(float(element.x)),
                "y": _float_str(float(element.y)),
                "text-anchor": element.anchor,
            }
        )
        return f"  <text {_attrs_to_str(attrs)}>{escape(element.text)}</text>"

    if isinstance(element, Formula):
        attrs.update(
            {
                "x": _float_str(float(element.x)),
                "y": _float_str(float(element.y)),
                "text-anchor": element.anchor,
                "data-formula": element.expr,
                "class": "formula-placeholder",
            }
        )
        return f"  <text {_attrs_to_str(attrs)}>{escape(element.expr)}</text>"

    raise TypeError(f"Unsupported element type: {type(element)!r}")


def compile_svg(problem: ProblemIR) -> str:
    sorted_elements = sorted(problem.elements, key=lambda e: e.z_index)
    width = _float_str(float(problem.width))
    height = _float_str(float(problem.height))

    lines: list[str] = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
        f"  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"{escape(problem.background, quote=True)}\" />",
    ]

    for element in sorted_elements:
        lines.append(_element_to_svg_line(element))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"
