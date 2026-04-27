from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import DrawElement, RenderRefs, RendererDocument, RenderViewBox

_DEFAULT_STROKE = "#111111"
_DEFAULT_FILL = "none"
_DEFAULT_TEXT_FILL = "#111111"
_DEFAULT_FONT_FAMILY = "Noto Sans KR, sans-serif"
_DEFAULT_FONT_SIZE = 26


@dataclass(frozen=True)
class _Frame:
    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class _ObjectExpansion:
    elements: tuple[DrawElement, ...]
    anchors: dict[str, tuple[float, float]]


def compile_renderer_from_layout(layout: dict[str, Any]) -> RendererDocument:
    if not isinstance(layout, dict):
        raise TypeError("layout must be an object")

    problem_id = str(layout.get("problem_id") or "problem")
    canvas = layout.get("canvas", {})
    if not isinstance(canvas, dict):
        canvas = {}
    width = float(canvas.get("width", 960))
    height = float(canvas.get("height", 640))
    background = canvas.get("background")
    resolved_background = background if isinstance(background, str) and background.strip() else "#FFFFFF"
    view_box = RenderViewBox(width=width, height=height, background=resolved_background)

    elements: list[DrawElement] = []
    if isinstance(layout.get("nodes"), list):
        elements.extend(_compile_legacy_nodes(layout))

    if isinstance(layout.get("slots"), list) or isinstance(layout.get("diagrams"), list):
        elements.extend(_compile_contract_layout(layout, width=width, height=height))

    return RendererDocument(problem_id=problem_id, view_box=view_box, elements=tuple(elements))


def compile_renderer_json(layout: dict[str, Any]) -> dict[str, Any]:
    return compile_renderer_from_layout(layout).to_dict()


def _compile_legacy_nodes(layout: dict[str, Any]) -> list[DrawElement]:
    nodes = layout.get("nodes", [])
    if not isinstance(nodes, list):
        return []
    sorted_nodes = sorted(
        [node for node in nodes if isinstance(node, dict)],
        key=lambda node: int(node.get("z_order", 0)) if isinstance(node.get("z_order"), int | float) else 0,
    )
    compiled: list[DrawElement] = []
    for node in sorted_nodes:
        element = _node_to_element(node)
        if element is not None:
            compiled.append(element)
    return compiled


def _node_to_element(node: dict[str, Any]) -> DrawElement | None:
    node_id = str(node.get("id") or "")
    if not node_id:
        return None
    node_type = str(node.get("type") or "")
    props = node.get("properties", {})
    if not isinstance(props, dict):
        props = {}
    refs = RenderRefs(layout_node_id=node_id)

    x = float(node.get("x", 0))
    y = float(node.get("y", 0))
    width = float(node.get("width", 0)) if isinstance(node.get("width"), int | float) else 0.0
    height = float(node.get("height", 0)) if isinstance(node.get("height"), int | float) else 0.0

    if node_type == "text":
        text = str(props.get("text", ""))
        text_type = "formula" if bool(props.get("is_formula")) else "text"
        return DrawElement(
            id=node_id,
            type=text_type,
            attributes=_text_style(props) | {"x": x, "y": y},
            source_ref=node.get("source_ref"),
            refs=refs,
            text=text,
        )

    if node_type == "group":
        raw_children = node.get("children", [])
        children: list[DrawElement] = []
        if isinstance(raw_children, list):
            sorted_children = sorted(
                [child for child in raw_children if isinstance(child, dict)],
                key=lambda child: int(child.get("z_order", 0))
                if isinstance(child.get("z_order"), int | float)
                else 0,
            )
            for child in sorted_children:
                compiled = _node_to_element(child)
                if compiled is not None:
                    children.append(compiled)
        return DrawElement(
            id=node_id,
            type="group",
            attributes={},
            source_ref=node.get("source_ref"),
            refs=refs,
            elements=tuple(children),
        )

    if node_type == "shape":
        object_type = props.get("object_type")
        if isinstance(object_type, str) and object_type.strip():
            expansion = _expand_object(
                object_id=node_id,
                object_type=object_type,
                object_data=props,
                frame=_Frame(x=x, y=y, width=max(width, 80.0), height=max(height, 80.0)),
                diagram_id=None,
            )
            return DrawElement(
                id=f"{node_id}.group",
                type="group",
                attributes={},
                source_ref=node.get("source_ref") if isinstance(node.get("source_ref"), str) else node_id,
                refs=refs,
                elements=expansion.elements,
            )
        return _shape_node_to_primitive(node_id=node_id, node=node, props=props, refs=refs)

    return DrawElement(
        id=node_id,
        type="rect",
        attributes={"x": x, "y": y, "width": max(width, 1.0), "height": max(height, 1.0), **_shape_style(props)},
        source_ref=node.get("source_ref"),
        refs=refs,
    )


def _shape_node_to_primitive(node_id: str, node: dict[str, Any], props: dict[str, Any], refs: RenderRefs) -> DrawElement:
    shape_type = str(props.get("shape_type") or "rect")
    x = float(node.get("x", 0))
    y = float(node.get("y", 0))
    style = _shape_style(props)
    source_ref = node.get("source_ref")
    if shape_type == "rect":
        attributes = {
            "x": x,
            "y": y,
            "width": float(node.get("width", 0)) if isinstance(node.get("width"), int | float) else 0,
            "height": float(node.get("height", 0)) if isinstance(node.get("height"), int | float) else 0,
            **style,
        }
        return DrawElement(id=node_id, type="rect", attributes=attributes, source_ref=source_ref, refs=refs)
    if shape_type == "circle":
        radius = float(props.get("r", 0)) if isinstance(props.get("r"), int | float) else 0
        return DrawElement(
            id=node_id,
            type="circle",
            attributes={"cx": x, "cy": y, "r": radius, **style},
            source_ref=source_ref,
            refs=refs,
        )
    if shape_type == "line":
        return DrawElement(
            id=node_id,
            type="line",
            attributes={
                "x1": float(props.get("x1", x)),
                "y1": float(props.get("y1", y)),
                "x2": float(props.get("x2", x)),
                "y2": float(props.get("y2", y)),
                **style,
            },
            source_ref=source_ref,
            refs=refs,
        )
    if shape_type == "polygon":
        points = props.get("points", [])
        return DrawElement(
            id=node_id,
            type="polygon",
            attributes={"points": points if isinstance(points, list) else [], **style},
            source_ref=source_ref,
            refs=refs,
        )
    if shape_type == "arc":
        return DrawElement(
            id=node_id,
            type="arc",
            attributes={
                "cx": x,
                "cy": y,
                "r": float(props.get("r", 0)),
                "start_angle": float(props.get("start_angle", 0)),
                "end_angle": float(props.get("end_angle", 180)),
                **style,
            },
            source_ref=source_ref,
            refs=refs,
        )
    if shape_type == "image":
        return DrawElement(
            id=node_id,
            type="image",
            attributes={
                "x": x,
                "y": y,
                "width": float(node.get("width", 0)) if isinstance(node.get("width"), int | float) else 0,
                "height": float(node.get("height", 0)) if isinstance(node.get("height"), int | float) else 0,
                "href": str(props.get("href", "")),
            },
            source_ref=source_ref,
            refs=refs,
        )
    if shape_type == "path":
        return DrawElement(
            id=node_id,
            type="fill_path",
            attributes={"d": str(props.get("d", "")), **style},
            source_ref=source_ref,
            refs=refs,
        )
    return DrawElement(
        id=node_id,
        type=shape_type,
        attributes={"x": x, "y": y, **style},
        source_ref=source_ref,
        refs=refs,
    )


def _compile_contract_layout(layout: dict[str, Any], *, width: float, height: float) -> list[DrawElement]:
    elements: list[DrawElement] = []
    slot_elements, slot_bottom = _compile_slots(layout, width=width)
    elements.extend(slot_elements)
    diagram_elements = _compile_diagrams(layout, width=width, height=height, start_y=max(slot_bottom + 28.0, 220.0))
    elements.extend(diagram_elements)
    return elements


def _compile_slots(layout: dict[str, Any], *, width: float) -> tuple[list[DrawElement], float]:
    slots = layout.get("slots", [])
    if not isinstance(slots, list):
        return [], 72.0

    ordered_slot_ids = _resolve_slot_order(layout)
    slot_by_id = {str(slot.get("id")): slot for slot in slots if isinstance(slot, dict) and isinstance(slot.get("id"), str)}

    y = 72.0
    x = 64.0
    max_text_width = max(width - 128.0, 200.0)
    elements: list[DrawElement] = []
    for slot_id in ordered_slot_ids:
        slot = slot_by_id.get(slot_id)
        if slot is None:
            continue
        kind = str(slot.get("kind", "text"))
        content = slot.get("content", {})
        if not isinstance(content, dict):
            content = {}
        refs = RenderRefs(layout_slot_id=slot_id)
        if kind == "text":
            text = str(content.get("text", ""))
            tx = float(content["x"]) if isinstance(content.get("x"), int | float) else x
            ty = float(content["y"]) if isinstance(content.get("y"), int | float) else y
            font_size = int(content["font_size"]) if isinstance(content.get("font_size"), int | float) else _DEFAULT_FONT_SIZE
            fill = str(content["fill"]) if isinstance(content.get("fill"), str) else _DEFAULT_TEXT_FILL
            font_family = str(content["font_family"]) if isinstance(content.get("font_family"), str) else _DEFAULT_FONT_FAMILY
            text_anchor = str(content["anchor"]) if isinstance(content.get("anchor"), str) else None
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "x": tx,
                "y": ty,
                "max_width": max_text_width,
                "fill": fill,
                "font-family": font_family,
                "font-size": font_size,
            }
            if text_anchor:
                attributes["text-anchor"] = text_anchor
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.text",
                    type="text",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                    text=text,
                )
            )
            if isinstance(content.get("y"), int | float):
                y = max(y, ty + 56.0)
            else:
                y += 56.0
            continue

        if kind == "choice":
            prompt = str(slot.get("prompt") or "")
            if prompt:
                elements.append(
                    DrawElement(
                        id=f"{slot_id}.prompt",
                        type="text",
                        attributes={
                            "x": x,
                            "y": y,
                            "fill": _DEFAULT_TEXT_FILL,
                            "font-family": _DEFAULT_FONT_FAMILY,
                            "font-size": 20,
                        },
                        source_ref=slot_id,
                        refs=refs,
                        text=prompt,
                    )
                )
                y += 34.0

            choices = content.get("choices", [])
            if isinstance(choices, list):
                for index, choice in enumerate(choices):
                    cy = y + index * 42.0
                    elements.append(
                        DrawElement(
                            id=f"{slot_id}.choice_marker.{index + 1}",
                            type="circle",
                            attributes={
                                "cx": x + 12.0,
                                "cy": cy - 7.0,
                                "r": 8.0,
                                "fill": "#ffffff",
                                "stroke": _DEFAULT_STROKE,
                                "stroke-width": 1.5,
                            },
                            source_ref=slot_id,
                            refs=refs,
                        )
                    )
                    elements.append(
                        DrawElement(
                            id=f"{slot_id}.choice_text.{index + 1}",
                            type="text",
                            attributes={
                                "x": x + 32.0,
                                "y": cy,
                                "fill": _DEFAULT_TEXT_FILL,
                                "font-family": _DEFAULT_FONT_FAMILY,
                                "font-size": 24,
                            },
                            source_ref=slot_id,
                            refs=refs,
                            text=str(choice),
                        )
                    )
                y += len(choices) * 42.0 + 18.0
            continue

        if kind == "blank":
            elements.append(
                DrawElement(
                    id=f"{slot_id}.blank",
                    type="rect",
                    attributes={
                        "x": x,
                        "y": y - 24.0,
                        "width": 120.0,
                        "height": 32.0,
                        "fill": "#ffffff",
                        "stroke": _DEFAULT_STROKE,
                        "stroke-width": 1.5,
                    },
                    source_ref=slot_id,
                    refs=refs,
                )
            )
            y += 48.0
            continue

        if kind == "label":
            elements.append(
                DrawElement(
                    id=f"{slot_id}.label",
                    type="text",
                    attributes={
                        "x": x,
                        "y": y,
                        "fill": _DEFAULT_TEXT_FILL,
                        "font-family": _DEFAULT_FONT_FAMILY,
                        "font-size": 20,
                    },
                    source_ref=slot_id,
                    refs=refs,
                    text=str(content.get("text", "")),
                )
            )
            y += 32.0
            continue

        if kind == "rect":
            x_pos = float(content.get("x", x))
            y_pos = float(content.get("y", y - 24.0))
            rw = float(content.get("width", 120.0))
            rh = float(content.get("height", 32.0))
            stroke = str(content.get("stroke", _DEFAULT_STROKE))
            fill = str(content.get("fill", "#ffffff"))
            stroke_width = float(content.get("stroke_width", 1.5))
            corner_rx = float(content["rx"]) if isinstance(content.get("rx"), int | float) else None
            corner_ry = float(content["ry"]) if isinstance(content.get("ry"), int | float) else None
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "x": x_pos,
                "y": y_pos,
                "width": rw,
                "height": rh,
                "fill": fill,
                "stroke": stroke,
                "stroke-width": stroke_width,
            }
            if corner_rx is not None:
                attributes["rx"] = corner_rx
            if corner_ry is not None:
                attributes["ry"] = corner_ry
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.rect",
                    type="rect",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                )
            )
            y = max(y, y_pos + rh + 16.0)
            continue

        if kind == "line":
            x1 = float(content.get("x1", x))
            y1 = float(content.get("y1", y))
            x2 = float(content.get("x2", x + 80.0))
            y2 = float(content.get("y2", y))
            stroke = str(content.get("stroke", _DEFAULT_STROKE))
            stroke_width = float(content.get("stroke_width", 2.0))
            stroke_dasharray = str(content["stroke_dasharray"]) if isinstance(content.get("stroke_dasharray"), str) else None
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "stroke": stroke,
                "stroke-width": stroke_width,
            }
            if stroke_dasharray:
                attributes["stroke-dasharray"] = stroke_dasharray
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.line",
                    type="line",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                )
            )
            y = max(y, max(y1, y2) + 16.0)
            continue

        if kind == "circle":
            cx = float(content.get("cx", x + 20.0))
            cy = float(content.get("cy", y))
            r = float(content.get("r", 10.0))
            stroke = str(content.get("stroke", _DEFAULT_STROKE))
            stroke_width = float(content.get("stroke_width", 2.0))
            fill = str(content.get("fill", "none"))
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "cx": cx,
                "cy": cy,
                "r": r,
                "stroke": stroke,
                "stroke-width": stroke_width,
                "fill": fill,
            }
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.circle",
                    type="circle",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                )
            )
            y = max(y, cy + r + 16.0)
            continue

        if kind == "polygon":
            points_raw = content.get("points")
            points: list[list[float]] = []
            if isinstance(points_raw, list):
                for point in points_raw:
                    if isinstance(point, (list, tuple)) and len(point) >= 2:
                        points.append([float(point[0]), float(point[1])])
            stroke = str(content.get("stroke", _DEFAULT_STROKE))
            stroke_width = float(content.get("stroke_width", 2.0))
            fill = str(content.get("fill", "none"))
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "points": points,
                "stroke": stroke,
                "stroke-width": stroke_width,
                "fill": fill,
            }
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.polygon",
                    type="polygon",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                )
            )
            continue

        if kind == "path":
            d = str(content.get("d", ""))
            stroke = str(content.get("stroke", _DEFAULT_STROKE))
            stroke_width = float(content.get("stroke_width", 2.0))
            stroke_dasharray = str(content["stroke_dasharray"]) if isinstance(content.get("stroke_dasharray"), str) else None
            fill = str(content.get("fill", "none"))
            semantic_role = str(content["semantic_role"]) if isinstance(content.get("semantic_role"), str) else None
            attributes: dict[str, Any] = {
                "d": d,
                "stroke": stroke,
                "stroke-width": stroke_width,
                "fill": fill,
            }
            if stroke_dasharray:
                attributes["stroke-dasharray"] = stroke_dasharray
            if semantic_role:
                attributes["data-semantic-role"] = semantic_role
            elements.append(
                DrawElement(
                    id=f"{slot_id}.path",
                    type="path",
                    attributes=attributes,
                    source_ref=slot_id,
                    refs=refs,
                )
            )

    return elements, y


def _resolve_slot_order(layout: dict[str, Any]) -> list[str]:
    regions = layout.get("regions", [])
    slots = layout.get("slots", [])
    slot_ids = [str(slot.get("id")) for slot in slots if isinstance(slot, dict) and isinstance(slot.get("id"), str)]
    seen: set[str] = set()
    ordered: list[str] = []
    if isinstance(regions, list):
        for region in regions:
            if not isinstance(region, dict):
                continue
            region_slot_ids = region.get("slot_ids", [])
            if not isinstance(region_slot_ids, list):
                continue
            for slot_id in region_slot_ids:
                if isinstance(slot_id, str) and slot_id in slot_ids and slot_id not in seen:
                    ordered.append(slot_id)
                    seen.add(slot_id)
    for slot_id in slot_ids:
        if slot_id not in seen:
            ordered.append(slot_id)
    return ordered


def _compile_diagrams(layout: dict[str, Any], *, width: float, height: float, start_y: float) -> list[DrawElement]:
    diagrams = layout.get("diagrams", [])
    if not isinstance(diagrams, list) or not diagrams:
        return []

    margin = 48.0
    gap = 18.0
    usable_height = max(height - start_y - margin, 180.0)
    each_height = max((usable_height - gap * (len(diagrams) - 1)) / max(len(diagrams), 1), 160.0)

    elements: list[DrawElement] = []
    for index, diagram in enumerate(diagrams):
        if not isinstance(diagram, dict):
            continue
        diagram_id = str(diagram.get("id") or f"diagram_{index + 1}")
        frame = _frame_from_layout(
            diagram.get("frame"),
            fallback=_Frame(
                x=margin,
                y=start_y + index * (each_height + gap),
                width=max(width - margin * 2, 320.0),
                height=each_height,
            ),
        )
        group_elements = _compile_single_diagram(diagram=diagram, diagram_id=diagram_id, frame=frame)
        elements.append(
            DrawElement(
                id=f"{diagram_id}.group",
                type="group",
                attributes={},
                source_ref=diagram_id,
                refs=RenderRefs(layout_diagram_id=diagram_id),
                elements=tuple(group_elements),
            )
        )
    return elements


def _compile_single_diagram(diagram: dict[str, Any], *, diagram_id: str, frame: _Frame) -> list[DrawElement]:
    objects = diagram.get("objects", [])
    label_slots = diagram.get("label_slots", [])
    if not isinstance(objects, list):
        objects = []
    if not isinstance(label_slots, list):
        label_slots = []

    object_count = max(len(objects), 1)
    cell_gap = 16.0
    cell_width = max((frame.width - cell_gap * (object_count - 1)) / object_count, 80.0)
    anchors_by_object: dict[str, dict[str, tuple[float, float]]] = {}

    elements: list[DrawElement] = []
    for index, obj in enumerate(objects):
        if not isinstance(obj, dict):
            continue
        object_id = str(obj.get("id") or f"{diagram_id}.obj_{index + 1}")
        object_type = str(obj.get("object_type") or "shape")
        default_object_frame = _Frame(
            x=frame.x + index * (cell_width + cell_gap),
            y=frame.y + 10.0,
            width=cell_width,
            height=max(frame.height - 20.0, 80.0),
        )
        object_frame = _frame_from_layout(obj.get("frame"), fallback=default_object_frame)
        expansion = _expand_object(
            object_id=object_id,
            object_type=object_type,
            object_data=obj,
            frame=object_frame,
            diagram_id=diagram_id,
        )
        anchors_by_object[object_id] = expansion.anchors
        elements.extend(expansion.elements)

    for label_slot in label_slots:
        if not isinstance(label_slot, dict):
            continue
        label_id = str(label_slot.get("id") or f"{diagram_id}.label")
        content = label_slot.get("content", {})
        if not isinstance(content, dict):
            content = {}
        text = str(content.get("text", ""))
        target_id = str(content.get("target_object_id", ""))
        target_anchor = str(content.get("target_anchor", "center"))
        x, y = _resolve_label_position(
            anchors=anchors_by_object.get(target_id, {}),
            frame=frame,
            anchor=target_anchor,
        )
        elements.append(
            DrawElement(
                id=f"{label_id}.text",
                type="text",
                attributes={
                    "x": x,
                    "y": y,
                    "fill": _DEFAULT_TEXT_FILL,
                    "font-family": _DEFAULT_FONT_FAMILY,
                    "font-size": 20,
                },
                source_ref=label_id,
                refs=RenderRefs(layout_slot_id=label_id, layout_diagram_id=diagram_id, layout_object_id=target_id or None),
                text=text,
            )
        )
    return elements


def _expand_object(
    *,
    object_id: str,
    object_type: str,
    object_data: dict[str, Any],
    frame: _Frame,
    diagram_id: str | None,
) -> _ObjectExpansion:
    refs = RenderRefs(layout_object_id=object_id, layout_diagram_id=diagram_id)
    source_ref = object_id
    object_type_normalized = object_type.strip().lower()

    if object_type_normalized == "cube":
        return _expand_cube(object_id=object_id, frame=frame, refs=refs, source_ref=source_ref)
    if object_type_normalized == "triangle":
        return _expand_triangle(object_id=object_id, frame=frame, refs=refs, source_ref=source_ref)
    if object_type_normalized == "circle":
        mark_center = bool(object_data.get("mark_center"))
        return _expand_circle_object(
            object_id=object_id,
            frame=frame,
            refs=refs,
            source_ref=source_ref,
            mark_center=mark_center,
        )
    if object_type_normalized == "grid":
        rows = int(object_data.get("rows", 1)) if isinstance(object_data.get("rows"), int | float) else 1
        cols = int(object_data.get("cols", 1)) if isinstance(object_data.get("cols"), int | float) else 1
        return _expand_grid(object_id=object_id, frame=frame, refs=refs, source_ref=source_ref, rows=rows, cols=cols)
    if object_type_normalized == "fraction_area_model":
        partitions = int(object_data.get("partitions", 2)) if isinstance(object_data.get("partitions"), int | float) else 2
        shaded = int(object_data.get("shaded", 1)) if isinstance(object_data.get("shaded"), int | float) else 1
        orientation = str(object_data.get("orientation", "horizontal"))
        return _expand_fraction_area_model(
            object_id=object_id,
            frame=frame,
            refs=refs,
            source_ref=source_ref,
            partitions=partitions,
            shaded=shaded,
            orientation=orientation,
        )
    if object_type_normalized == "arrow":
        direction = str(object_data.get("direction", "right"))
        return _expand_arrow(object_id=object_id, frame=frame, refs=refs, source_ref=source_ref, direction=direction)
    return _expand_fallback_box(object_id=object_id, frame=frame, refs=refs, source_ref=source_ref)


def _expand_cube(*, object_id: str, frame: _Frame, refs: RenderRefs, source_ref: str) -> _ObjectExpansion:
    offset = max(min(frame.width, frame.height) * 0.22, 14.0)
    bx, by = frame.x + 8.0, frame.y + 8.0
    bw, bh = max(frame.width - offset - 16.0, 24.0), max(frame.height - offset - 16.0, 24.0)
    fx, fy = bx + offset, by + offset

    def line(eid: str, x1: float, y1: float, x2: float, y2: float, hidden: bool = False) -> DrawElement:
        attrs = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": _DEFAULT_STROKE, "stroke-width": 2}
        if hidden:
            attrs["stroke-dasharray"] = "6 4"
            attrs["opacity"] = 0.65
        return DrawElement(id=eid, type="line", attributes=attrs, source_ref=source_ref, refs=refs)

    elements = (
        line(f"{object_id}.edge.back.top", bx, by, bx + bw, by),
        line(f"{object_id}.edge.back.left", bx, by, bx, by + bh),
        line(f"{object_id}.edge.back.right", bx + bw, by, bx + bw, by + bh, hidden=True),
        line(f"{object_id}.edge.back.bottom", bx, by + bh, bx + bw, by + bh, hidden=True),
        line(f"{object_id}.edge.front.top", fx, fy, fx + bw, fy),
        line(f"{object_id}.edge.front.left", fx, fy, fx, fy + bh),
        line(f"{object_id}.edge.front.right", fx + bw, fy, fx + bw, fy + bh),
        line(f"{object_id}.edge.front.bottom", fx, fy + bh, fx + bw, fy + bh),
        line(f"{object_id}.edge.connect.tl", bx, by, fx, fy),
        line(f"{object_id}.edge.connect.tr", bx + bw, by, fx + bw, fy),
        line(f"{object_id}.edge.connect.bl", bx, by + bh, fx, fy + bh, hidden=True),
        line(f"{object_id}.edge.connect.br", bx + bw, by + bh, fx + bw, fy + bh),
    )
    anchors = {
        "center": (fx + bw / 2.0, fy + bh / 2.0),
        "right": (fx + bw + 16.0, fy + bh / 2.0),
        "left": (bx - 8.0, fy + bh / 2.0),
        "top": (fx + bw / 2.0, by - 8.0),
        "bottom": (fx + bw / 2.0, fy + bh + 22.0),
    }
    return _ObjectExpansion(elements=elements, anchors=anchors)


def _expand_triangle(*, object_id: str, frame: _Frame, refs: RenderRefs, source_ref: str) -> _ObjectExpansion:
    top = [frame.x + frame.width / 2.0, frame.y + 8.0]
    left = [frame.x + 8.0, frame.y + frame.height - 8.0]
    right = [frame.x + frame.width - 8.0, frame.y + frame.height - 8.0]
    element = DrawElement(
        id=f"{object_id}.polygon",
        type="polygon",
        attributes={"points": [top, left, right], "fill": _DEFAULT_FILL, "stroke": _DEFAULT_STROKE, "stroke-width": 2},
        source_ref=source_ref,
        refs=refs,
    )
    anchors = {
        "center": ((top[0] + left[0] + right[0]) / 3.0, (top[1] + left[1] + right[1]) / 3.0),
        "top": (top[0], top[1] - 10.0),
        "left": (left[0] - 12.0, left[1]),
        "right": (right[0] + 8.0, right[1]),
    }
    return _ObjectExpansion(elements=(element,), anchors=anchors)


def _expand_circle_object(
    *,
    object_id: str,
    frame: _Frame,
    refs: RenderRefs,
    source_ref: str,
    mark_center: bool,
) -> _ObjectExpansion:
    cx = frame.x + frame.width / 2.0
    cy = frame.y + frame.height / 2.0
    r = max(min(frame.width, frame.height) / 2.0 - 10.0, 8.0)
    circle = DrawElement(
        id=f"{object_id}.circle",
        type="circle",
        attributes={"cx": cx, "cy": cy, "r": r, "fill": _DEFAULT_FILL, "stroke": _DEFAULT_STROKE, "stroke-width": 2},
        source_ref=source_ref,
        refs=refs,
    )
    elements: list[DrawElement] = [circle]
    if mark_center:
        elements.append(
            DrawElement(
                id=f"{object_id}.center",
                type="circle",
                attributes={"cx": cx, "cy": cy, "r": 3.0, "fill": _DEFAULT_STROKE, "stroke": _DEFAULT_STROKE, "stroke-width": 1},
                source_ref=source_ref,
                refs=refs,
            )
        )
    anchors = {
        "center": (cx, cy),
        "top": (cx, cy - r - 8.0),
        "bottom": (cx, cy + r + 18.0),
        "left": (cx - r - 12.0, cy),
        "right": (cx + r + 8.0, cy),
    }
    return _ObjectExpansion(elements=tuple(elements), anchors=anchors)


def _expand_grid(
    *,
    object_id: str,
    frame: _Frame,
    refs: RenderRefs,
    source_ref: str,
    rows: int,
    cols: int,
) -> _ObjectExpansion:
    rows = max(rows, 1)
    cols = max(cols, 1)
    x = frame.x + 8.0
    y = frame.y + 8.0
    w = max(frame.width - 16.0, 20.0)
    h = max(frame.height - 16.0, 20.0)

    elements: list[DrawElement] = [
        DrawElement(
            id=f"{object_id}.grid.boundary",
            type="rect",
            attributes={"x": x, "y": y, "width": w, "height": h, "fill": _DEFAULT_FILL, "stroke": _DEFAULT_STROKE, "stroke-width": 2},
            source_ref=source_ref,
            refs=refs,
        )
    ]

    for col in range(1, cols):
        vx = x + (w / cols) * col
        elements.append(
            DrawElement(
                id=f"{object_id}.grid.v.{col}",
                type="line",
                attributes={"x1": vx, "y1": y, "x2": vx, "y2": y + h, "stroke": _DEFAULT_STROKE, "stroke-width": 1.5},
                source_ref=source_ref,
                refs=refs,
            )
        )
    for row in range(1, rows):
        hy = y + (h / rows) * row
        elements.append(
            DrawElement(
                id=f"{object_id}.grid.h.{row}",
                type="line",
                attributes={"x1": x, "y1": hy, "x2": x + w, "y2": hy, "stroke": _DEFAULT_STROKE, "stroke-width": 1.5},
                source_ref=source_ref,
                refs=refs,
            )
        )
    anchors = {"center": (x + w / 2.0, y + h / 2.0), "top": (x + w / 2.0, y - 8.0), "right": (x + w + 8.0, y + h / 2.0)}
    return _ObjectExpansion(elements=tuple(elements), anchors=anchors)


def _expand_fraction_area_model(
    *,
    object_id: str,
    frame: _Frame,
    refs: RenderRefs,
    source_ref: str,
    partitions: int,
    shaded: int,
    orientation: str,
) -> _ObjectExpansion:
    partitions = max(partitions, 1)
    shaded = min(max(shaded, 0), partitions)
    x = frame.x + 8.0
    y = frame.y + 8.0
    w = max(frame.width - 16.0, 20.0)
    h = max(frame.height - 16.0, 20.0)
    horizontal = orientation.strip().lower() != "vertical"

    elements: list[DrawElement] = [
        DrawElement(
            id=f"{object_id}.fraction.boundary",
            type="rect",
            attributes={"x": x, "y": y, "width": w, "height": h, "fill": _DEFAULT_FILL, "stroke": _DEFAULT_STROKE, "stroke-width": 2},
            source_ref=source_ref,
            refs=refs,
        )
    ]

    for index in range(1, partitions):
        if horizontal:
            px = x + (w / partitions) * index
            elements.append(
                DrawElement(
                    id=f"{object_id}.fraction.partition.{index}",
                    type="line",
                    attributes={"x1": px, "y1": y, "x2": px, "y2": y + h, "stroke": _DEFAULT_STROKE, "stroke-width": 1.2},
                    source_ref=source_ref,
                    refs=refs,
                )
            )
        else:
            py = y + (h / partitions) * index
            elements.append(
                DrawElement(
                    id=f"{object_id}.fraction.partition.{index}",
                    type="line",
                    attributes={"x1": x, "y1": py, "x2": x + w, "y2": py, "stroke": _DEFAULT_STROKE, "stroke-width": 1.2},
                    source_ref=source_ref,
                    refs=refs,
                )
            )

    for index in range(shaded):
        if horizontal:
            sx = x + (w / partitions) * index
            elements.append(
                DrawElement(
                    id=f"{object_id}.fraction.shaded.{index + 1}",
                    type="rect",
                    attributes={
                        "x": sx,
                        "y": y,
                        "width": w / partitions,
                        "height": h,
                        "fill": "#D9E8FF",
                        "stroke": "none",
                    },
                    source_ref=source_ref,
                    refs=refs,
                )
            )
        else:
            sy = y + (h / partitions) * index
            elements.append(
                DrawElement(
                    id=f"{object_id}.fraction.shaded.{index + 1}",
                    type="rect",
                    attributes={
                        "x": x,
                        "y": sy,
                        "width": w,
                        "height": h / partitions,
                        "fill": "#D9E8FF",
                        "stroke": "none",
                    },
                    source_ref=source_ref,
                    refs=refs,
                )
            )

    anchors = {"center": (x + w / 2.0, y + h / 2.0), "right": (x + w + 10.0, y + h / 2.0), "top": (x + w / 2.0, y - 8.0)}
    return _ObjectExpansion(elements=tuple(elements), anchors=anchors)


def _expand_arrow(
    *,
    object_id: str,
    frame: _Frame,
    refs: RenderRefs,
    source_ref: str,
    direction: str,
) -> _ObjectExpansion:
    direction = direction.strip().lower()
    x = frame.x + 8.0
    y = frame.y + 8.0
    w = max(frame.width - 16.0, 20.0)
    h = max(frame.height - 16.0, 20.0)
    cx = x + w / 2.0
    cy = y + h / 2.0
    head = 16.0

    if direction == "left":
        line = (x + w, cy, x + head, cy)
        head_points = [[x, cy], [x + head, cy - 8.0], [x + head, cy + 8.0]]
        anchor = (x - 8.0, cy)
    elif direction == "up":
        line = (cx, y + h, cx, y + head)
        head_points = [[cx, y], [cx - 8.0, y + head], [cx + 8.0, y + head]]
        anchor = (cx, y - 8.0)
    elif direction == "down":
        line = (cx, y, cx, y + h - head)
        head_points = [[cx, y + h], [cx - 8.0, y + h - head], [cx + 8.0, y + h - head]]
        anchor = (cx, y + h + 10.0)
    else:
        line = (x, cy, x + w - head, cy)
        head_points = [[x + w, cy], [x + w - head, cy - 8.0], [x + w - head, cy + 8.0]]
        anchor = (x + w + 8.0, cy)

    elements = (
        DrawElement(
            id=f"{object_id}.arrow.body",
            type="line",
            attributes={"x1": line[0], "y1": line[1], "x2": line[2], "y2": line[3], "stroke": _DEFAULT_STROKE, "stroke-width": 2},
            source_ref=source_ref,
            refs=refs,
        ),
        DrawElement(
            id=f"{object_id}.arrow.head",
            type="polygon",
            attributes={"points": head_points, "fill": _DEFAULT_STROKE, "stroke": _DEFAULT_STROKE, "stroke-width": 1.5},
            source_ref=source_ref,
            refs=refs,
        ),
    )
    anchors = {"center": (cx, cy), "tip": anchor, "right": (x + w + 8.0, cy), "top": (cx, y - 8.0)}
    return _ObjectExpansion(elements=elements, anchors=anchors)


def _expand_fallback_box(*, object_id: str, frame: _Frame, refs: RenderRefs, source_ref: str) -> _ObjectExpansion:
    element = DrawElement(
        id=f"{object_id}.box",
        type="rect",
        attributes={
            "x": frame.x + 8.0,
            "y": frame.y + 8.0,
            "width": max(frame.width - 16.0, 20.0),
            "height": max(frame.height - 16.0, 20.0),
            "fill": _DEFAULT_FILL,
            "stroke": _DEFAULT_STROKE,
            "stroke-width": 2,
        },
        source_ref=source_ref,
        refs=refs,
    )
    anchors = {"center": (frame.x + frame.width / 2.0, frame.y + frame.height / 2.0)}
    return _ObjectExpansion(elements=(element,), anchors=anchors)


def _resolve_label_position(
    *,
    anchors: dict[str, tuple[float, float]],
    frame: _Frame,
    anchor: str,
) -> tuple[float, float]:
    if not anchors:
        return frame.x + 12.0, frame.y + 24.0
    if anchor in anchors:
        return anchors[anchor]
    return anchors.get("center", (frame.x + frame.width / 2.0, frame.y + frame.height / 2.0))


def _frame_from_layout(raw_frame: Any, *, fallback: _Frame) -> _Frame:
    if not isinstance(raw_frame, dict):
        return fallback

    x = float(raw_frame.get("x", fallback.x)) if isinstance(raw_frame.get("x"), int | float) else fallback.x
    y = float(raw_frame.get("y", fallback.y)) if isinstance(raw_frame.get("y"), int | float) else fallback.y
    width = (
        float(raw_frame.get("width", fallback.width))
        if isinstance(raw_frame.get("width"), int | float)
        else fallback.width
    )
    height = (
        float(raw_frame.get("height", fallback.height))
        if isinstance(raw_frame.get("height"), int | float)
        else fallback.height
    )
    return _Frame(x=x, y=y, width=max(width, 1.0), height=max(height, 1.0))


def _shape_style(props: dict[str, Any]) -> dict[str, Any]:
    stroke = props.get("stroke") if isinstance(props.get("stroke"), str) else _DEFAULT_STROKE
    fill = props.get("fill") if isinstance(props.get("fill"), str) else _DEFAULT_FILL
    stroke_width = float(props.get("stroke_width", 1.5)) if isinstance(props.get("stroke_width"), int | float) else 1.5
    style: dict[str, Any] = {"stroke": stroke, "fill": fill, "stroke-width": stroke_width}
    if isinstance(props.get("opacity"), int | float):
        style["opacity"] = float(props["opacity"])
    if isinstance(props.get("stroke_dasharray"), str):
        style["stroke-dasharray"] = props["stroke_dasharray"]
    return style


def _text_style(props: dict[str, Any]) -> dict[str, Any]:
    fill = props.get("fill") if isinstance(props.get("fill"), str) else _DEFAULT_TEXT_FILL
    family = props.get("font_family") if isinstance(props.get("font_family"), str) else _DEFAULT_FONT_FAMILY
    size = float(props.get("font_size", _DEFAULT_FONT_SIZE)) if isinstance(props.get("font_size"), int | float) else _DEFAULT_FONT_SIZE
    style: dict[str, Any] = {"fill": fill, "font-family": family, "font-size": size}
    if isinstance(props.get("font_weight"), str):
        style["font-weight"] = props["font_weight"]
    if isinstance(props.get("font_style"), str):
        style["font-style"] = props["font_style"]
    if isinstance(props.get("opacity"), int | float):
        style["opacity"] = float(props["opacity"])
    return style
