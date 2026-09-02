from __future__ import annotations

import copy
from typing import Any


def sanitize_layout(
    layout: dict[str, Any],
    *,
    deleted_slots: set[str] | None = None,
    protected_slot_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Apply final layout invariants before rendering or writing artifacts."""
    sanitized = copy.deepcopy(layout)
    deleted_slots = deleted_slots or set()
    protected_slot_ids = protected_slot_ids or set()
    slots = sanitized.get("slots")
    if not isinstance(slots, list):
        sanitized["slots"] = []
        slots = sanitized["slots"]

    clean_slots: list[dict[str, Any]] = []
    canvas_box = _canvas_box(sanitized.get("canvas"))
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        if (
            isinstance(slot_id, str)
            and slot_id not in protected_slot_ids
            and _deleted_slot_matches(slot_id, deleted_slots)
        ):
            continue
        content = slot.get("content")
        if isinstance(content, dict) and is_submitted_answer_slot(slot):
            sanitize_answer_input_content(content)
            _clamp_box_content_to_canvas(content, canvas_box)
        clean_slots.append(slot)
    _separate_top_text_from_following_slots(
        clean_slots,
        canvas_box,
        regions=sanitized.get("regions"),
        groups=sanitized.get("groups"),
        protected_slot_ids=protected_slot_ids,
    )
    sanitized["slots"] = clean_slots

    slot_ids = {slot["id"] for slot in clean_slots if isinstance(slot.get("id"), str)}
    sanitized["regions"] = _sanitize_regions(sanitized.get("regions"), slot_ids)
    sanitized["groups"] = _sanitize_groups(sanitized.get("groups"), slot_ids)
    sanitized["reading_order"] = _sanitize_reading_order(
        sanitized.get("reading_order"),
        slot_ids,
        {
            region["id"]
            for region in sanitized["regions"]
            if isinstance(region.get("id"), str)
        },
    )
    return sanitized


def sanitize_answer_input_content(content: dict[str, Any]) -> None:
    """Normalize answer input rectangles so author/editor styles cannot hide them."""
    interaction = content.get("interaction")
    if not isinstance(interaction, dict):
        return
    if interaction.get("type") != "input" or interaction.get("role") != "answer":
        return

    if "text" not in content:
        content["fill"] = "#ffffff"
        content["stroke"] = (
            content.get("stroke")
            if isinstance(content.get("stroke"), str)
            else "#111827"
        )
        content["stroke_width"] = (
            content.get("stroke_width")
            if isinstance(content.get("stroke_width"), int | float)
            else 1.2
        )
    interaction.setdefault("include_in_submission", True)
    interaction.setdefault("group_id", "final_answer")

    width = content.get("width")
    height = content.get("height")
    input_style = content.get("input_style")
    if not isinstance(input_style, dict):
        input_style = {}
        content["input_style"] = input_style
    if isinstance(width, int | float):
        input_style.setdefault("width", round(float(width), 3))
    if isinstance(height, int | float):
        input_style.setdefault("height", round(float(height), 3))
    input_style.setdefault("font_size_mode", "auto")
    input_style.setdefault("font_size_adjust", 0)
    input_style.setdefault("min_font_size", 14)
    input_style.setdefault("max_font_size", 52)
    input_style.setdefault("font_weight", 700)
    input_style.setdefault("horizontal_align", "center")
    input_style.setdefault("vertical_align", "middle")
    input_style.setdefault("text_color", "#222222")


def _canvas_box(canvas: Any) -> tuple[float, float] | None:
    if not isinstance(canvas, dict):
        return None
    width = canvas.get("width")
    height = canvas.get("height")
    if not isinstance(width, int | float) or not isinstance(height, int | float):
        return None
    if width <= 0 or height <= 0:
        return None
    return float(width), float(height)


def _clamp_box_content_to_canvas(
    content: dict[str, Any],
    canvas_box: tuple[float, float] | None,
) -> None:
    if canvas_box is None:
        return
    x = content.get("x")
    y = content.get("y")
    width = content.get("width")
    height = content.get("height")
    if not all(isinstance(value, int | float) for value in (x, y, width, height)):
        return
    canvas_width, canvas_height = canvas_box
    margin = 8.0
    clean_width = min(float(width), max(1.0, canvas_width - margin * 2))
    clean_height = min(float(height), max(1.0, canvas_height - margin * 2))
    max_x = max(margin, canvas_width - clean_width - margin)
    max_y = max(margin, canvas_height - clean_height - margin)
    clamped_x = min(max(float(x), margin), max_x)
    clamped_y = min(max(float(y), margin), max_y)
    content["x"] = round(clamped_x, 3)
    content["y"] = round(clamped_y, 3)
    content["width"] = round(clean_width, 3)
    content["height"] = round(clean_height, 3)
    input_style = content.get("input_style")
    if isinstance(input_style, dict):
        input_style["width"] = round(clean_width, 3)
        input_style["height"] = round(clean_height, 3)


def _separate_top_text_from_following_slots(
    slots: list[dict[str, Any]],
    canvas_box: tuple[float, float] | None,
    *,
    regions: list[dict[str, Any]] | None = None,
    groups: list[dict[str, Any]] | None = None,
    protected_slot_ids: set[str],
) -> None:
    if canvas_box is None:
        return
    _, canvas_height = canvas_box
    top_text_bottom = _top_text_bottom(slots)
    if top_text_bottom is None:
        return

    slot_id_to_slot = {
        slot["id"]: slot
        for slot in slots
        if isinstance(slot, dict) and isinstance(slot.get("id"), str)
    }

    parent: dict[str, str] = {}

    def find(s: str) -> str:
        parent.setdefault(s, s)
        if parent[s] != s:
            parent[s] = find(parent[s])
        return parent[s]

    def union(a: str, b: str) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_a] = root_b

    # Cluster by region (non-stem/header)
    if isinstance(regions, list):
        for region in regions:
            if not isinstance(region, dict):
                continue
            role = region.get("role")
            region_id = str(region.get("id") or "")
            if role == "stem" or "header" in region_id:
                continue
            r_slots = [
                s
                for s in region.get("slot_ids", [])
                if isinstance(s, str) and s in slot_id_to_slot
            ]
            for i in range(1, len(r_slots)):
                union(r_slots[0], r_slots[i])

    # Cluster by group
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, dict):
                continue
            members = [
                s
                for s in group.get("member_ids", [])
                if isinstance(s, str) and s in slot_id_to_slot
            ]
            for i in range(1, len(members)):
                union(members[0], members[i])

    # Cluster by compound prefixes (e.g. table, graphpaper, konva)
    prefix_to_slots: dict[str, list[str]] = {}
    for slot_id in slot_id_to_slot:
        prefix = _cohesive_slot_prefix(slot_id)
        if prefix:
            prefix_to_slots.setdefault(prefix, []).append(slot_id)
    for p_slots in prefix_to_slots.values():
        for i in range(1, len(p_slots)):
            union(p_slots[0], p_slots[i])

    clusters_by_root: dict[str, list[dict[str, Any]]] = {}
    for slot_id, slot in slot_id_to_slot.items():
        root = find(slot_id)
        clusters_by_root.setdefault(root, []).append(slot)

    margin = 8.0
    clear_y = top_text_bottom + margin

    colliding_clusters: list[list[dict[str, Any]]] = []

    for cluster in clusters_by_root.values():
        if any(_is_top_text_slot(s) for s in cluster):
            continue

        is_cluster_protected = False
        for s in cluster:
            sid = s.get("id")
            if (
                sid in protected_slot_ids
                or (isinstance(sid, str) and sid.startswith("konva_"))
                or is_submitted_answer_slot(s)
            ):
                is_cluster_protected = True
                break
        if is_cluster_protected:
            continue

        cluster_collides = False
        for s in cluster:
            box = _slot_box(s)
            if box is None:
                continue
            _, y, _, height = box
            if y < clear_y and y + height > top_text_bottom:
                cluster_collides = True
                break

        if cluster_collides:
            colliding_clusters.append(cluster)

    if not colliding_clusters:
        return

    boxes: list[tuple[float, float, float, float]] = []
    all_colliding_slots: list[dict[str, Any]] = []
    for cluster in colliding_clusters:
        for s in cluster:
            all_colliding_slots.append(s)
            box = _slot_box(s)
            if box is not None:
                boxes.append(box)

    if not boxes:
        return

    min_y = min(b[1] for b in boxes)
    max_bottom = max(b[1] + b[3] for b in boxes)
    dy = clear_y - min_y
    if dy <= 0:
        return
    bottom_limit = canvas_height - margin
    if max_bottom + dy > bottom_limit:
        dy = max(0.0, bottom_limit - max_bottom)
    if dy <= 0:
        return

    shifted_ids: set[str] = set()
    for s in all_colliding_slots:
        sid = s.get("id")
        if not isinstance(sid, str) or sid in shifted_ids:
            continue
        shifted_ids.add(sid)
        content = s.get("content")
        if isinstance(content, dict):
            _shift_content_y(content, dy)


def _top_text_bottom(slots: list[dict[str, Any]]) -> float | None:
    bottoms: list[float] = []
    for slot in slots:
        if not _is_top_text_slot(slot):
            continue
        box = _slot_box(slot)
        if box is not None:
            bottoms.append(box[1] + box[3])
    return max(bottoms) if bottoms else None


def _is_top_text_slot(slot: dict[str, Any]) -> bool:
    content = slot.get("content")
    if not isinstance(content, dict) or not isinstance(content.get("text"), str):
        return False
    if slot.get("kind") != "text_box":
        return False
    y = content.get("y")
    height = content.get("height")
    width = content.get("width")
    if not all(isinstance(value, int | float) for value in (y, height, width)):
        return False
    if float(y) > 40 or float(height) < 60 or float(width) < 240:
        return False
    interaction = content.get("interaction")
    return not (
        isinstance(interaction, dict)
        and interaction.get("type") == "input"
        and interaction.get("role") == "answer"
    )


def _slot_box(slot: dict[str, Any]) -> tuple[float, float, float, float] | None:
    content = slot.get("content")
    if not isinstance(content, dict):
        return None
    kind = slot.get("kind")
    if kind in {"rect", "text_box", "image"}:
        x = content.get("x")
        y = content.get("y")
        width = content.get("width")
        height = content.get("height")
        if all(isinstance(value, int | float) for value in (x, y, width, height)):
            return (float(x), float(y), float(width), float(height))
    if kind == "text":
        x = content.get("x")
        y = content.get("y")
        font_size = content.get("font_size")
        max_width = content.get("max_width")
        if isinstance(x, int | float) and isinstance(y, int | float):
            height = float(font_size) if isinstance(font_size, int | float) else 18.0
            width = float(max_width) if isinstance(max_width, int | float) else height
            return (float(x), float(y) - height * 0.85, width, height * 1.05)
    if kind == "line":
        x1 = content.get("x1")
        y1 = content.get("y1")
        x2 = content.get("x2")
        y2 = content.get("y2")
        if all(isinstance(value, int | float) for value in (x1, y1, x2, y2)):
            left = min(float(x1), float(x2))
            top = min(float(y1), float(y2))
            return (left, top, abs(float(x2) - float(x1)), abs(float(y2) - float(y1)))
    if kind == "circle":
        cx = content.get("cx")
        cy = content.get("cy")
        r = content.get("r")
        if all(isinstance(value, int | float) for value in (cx, cy, r)):
            radius = float(r)
            return (float(cx) - radius, float(cy) - radius, radius * 2, radius * 2)
    return None


def _shift_content_y(content: dict[str, Any], dy: float) -> None:
    for key in ("y", "cy", "y1", "y2"):
        value = content.get(key)
        if isinstance(value, int | float):
            content[key] = round(float(value) + dy, 3)
    input_style = content.get("input_style")
    if isinstance(input_style, dict):
        y = input_style.get("y")
        if isinstance(y, int | float):
            input_style["y"] = round(float(y) + dy, 3)


def _cohesive_slot_prefix(slot_id: Any) -> str | None:
    if not isinstance(slot_id, str):
        return None
    if slot_id.startswith("konva_"):
        prefix, _, _ = slot_id.rpartition("_")
        if prefix:
            return prefix + "_"
        return slot_id
    parts = slot_id.split(".")
    if len(parts) >= 3 and parts[0] == "slot":
        return f"{parts[0]}.{parts[1]}."
    return None


def is_submitted_answer_slot(slot: dict[str, Any]) -> bool:
    content = slot.get("content")
    interaction = content.get("interaction") if isinstance(content, dict) else None
    return (
        isinstance(interaction, dict)
        and interaction.get("type") == "input"
        and interaction.get("role") == "answer"
        and interaction.get("include_in_submission") is not False
    )


def _sanitize_regions(value: Any, slot_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for region in value:
        if not isinstance(region, dict):
            continue
        region_id = region.get("id")
        if not isinstance(region_id, str):
            continue
        clean = dict(region)
        clean["slot_ids"] = [
            slot_id
            for slot_id in region.get("slot_ids", [])
            if isinstance(slot_id, str) and slot_id in slot_ids
        ]
        out.append(clean)
    return out


def _sanitize_groups(value: Any, slot_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for group in value:
        if not isinstance(group, dict):
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str):
            continue
        clean = dict(group)
        clean["member_ids"] = [
            slot_id
            for slot_id in group.get("member_ids", [])
            if isinstance(slot_id, str) and slot_id in slot_ids
        ]
        out.append(clean)
    return out


def _sanitize_reading_order(
    value: Any,
    slot_ids: set[str],
    region_ids: set[str],
) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or item in seen:
            continue
        if item in slot_ids or item in region_ids or item.startswith("diagram."):
            out.append(item)
            seen.add(item)
    return out


def _deleted_slot_matches(slot_id: str, deleted_slots: set[str]) -> bool:
    if slot_id in deleted_slots:
        return True
    for deleted in deleted_slots:
        if slot_id.startswith(f"{deleted}."):
            suffix = slot_id[len(deleted) + 1 :]
            if suffix in {
                "num",
                "den",
                "bar",
                "whole",
                "box",
                "text",
                "rect",
                "line",
                "circle",
                "label",
                "left",
                "right",
                "middle",
                "inner",
                "outer",
            }:
                return True
    return False
