from __future__ import annotations

import copy
import re
from typing import Any

from modu_math.layout.sanitizer import sanitize_answer_input_content

_CONTEXT_TOKENS = ("example", "reference", "legend")
_CONTEXT_REGION_ROLES = {"example", "reference", "given", "legend"}


def project_suffixed_subproblem(
    *,
    artifact_id: str,
    template_id: str | None,
    layout: dict[str, Any],
    semantic: dict[str, Any],
    solvable: dict[str, Any] | None,
    protected_slot_ids: set[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None, set[str]]:
    """Keep only the matching ``group.problem_N`` for copied ``*_N`` files.

    Some editor split flows copy the original DSL into ``problem_1``,
    ``problem_2``, ... files without writing an override file. When the copied
    DSL still has the original base problem id and explicit problem groups, the
    build can safely project the artifact to the suffix-selected group.
    """
    index = _artifact_suffix_index(artifact_id, template_id)
    if index is None:
        return layout, semantic, solvable, set()

    groups = [group for group in layout.get("groups", []) if isinstance(group, dict)]
    group_id = _target_group_id(groups, index)
    regions = [
        region for region in layout.get("regions", []) if isinstance(region, dict)
    ]
    region_id = None if group_id is not None else _target_region_id(regions, index)
    target_container = (
        next((group for group in groups if group.get("id") == group_id), None)
        if group_id is not None
        else next((region for region in regions if region.get("id") == region_id), None)
    )
    if not isinstance(target_container, dict):
        return layout, semantic, solvable, set()

    target_members = {
        slot_id
        for slot_id in (
            target_container.get("member_ids") or target_container.get("slot_ids") or []
        )
        if isinstance(slot_id, str)
    }
    if not target_members:
        return layout, semantic, solvable, set()

    slots = [slot for slot in layout.get("slots", []) if isinstance(slot, dict)]
    slot_by_id = {slot["id"]: slot for slot in slots if isinstance(slot.get("id"), str)}
    all_group_members = {
        slot_id
        for group in groups
        for slot_id in group.get("member_ids", [])
        if isinstance(slot_id, str)
    }
    stem_ids = _stem_slot_ids(layout)
    context_ids = _context_slot_ids(layout, groups)
    protected_slot_ids = protected_slot_ids or set()
    fixed_ids = stem_ids | context_ids | protected_slot_ids
    all_submit_slot_ids = _all_submit_slot_ids(slots)
    structural_target_members = target_members - all_submit_slot_ids
    target_box = _union_box(
        [
            _slot_box(slot_by_id.get(slot_id))
            for slot_id in (structural_target_members or target_members)
        ]
    )
    problem_answer_ids = _answer_slot_ids_for_problem(semantic.get("answer"), index)
    problem_answer_ids |= _answer_slot_ids_for_target_members(
        target_members, slot_by_id
    )
    spatial_answer_input_ids = _target_answer_input_slot_ids(slots, target_box)
    keep_ids = fixed_ids | target_members | problem_answer_ids
    if isinstance(solvable, dict):
        problem_answer_ids |= _answer_slot_ids_for_problem(
            solvable.get("answer"), index
        )
        keep_ids |= problem_answer_ids

    if target_box is not None:
        for slot in slots:
            slot_id = slot.get("id")
            if not isinstance(slot_id, str) or slot_id in keep_ids:
                continue
            slot_problem_index = _identifier_problem_index(slot_id)
            if slot_problem_index is not None and slot_problem_index != index:
                continue
            if slot_id in all_group_members:
                continue
            if _slot_kind(slot) in {"rect", "circle", "path", "line"}:
                box = _slot_box(slot)
                if box is not None and _box_center_in(box, target_box, margin=12.0):
                    keep_ids.add(slot_id)

    target_submit_ids = {
        slot_id
        for slot_id in all_submit_slot_ids
        if slot_id in target_members
        or _identifier_problem_index(slot_id) == index
    }
    if not target_submit_ids:
        target_submit_ids = _submit_slot_ids_for_index(slots, index)
    if not target_submit_ids:
        target_submit_ids = spatial_answer_input_ids

    rebound_submit_ids = _rebind_stray_ordered_submit_slots(
        ordered_submit_ids=target_submit_ids,
        target_members=target_members,
        target_box=target_box,
        slot_by_id=slot_by_id,
        answer=semantic.get("answer"),
        index=index,
    )
    if rebound_submit_ids:
        keep_ids -= target_submit_ids
        target_submit_ids = rebound_submit_ids
        problem_answer_ids |= rebound_submit_ids

    if target_submit_ids:
        keep_ids -= all_submit_slot_ids - target_submit_ids
        keep_ids |= target_submit_ids
        problem_answer_ids |= target_submit_ids

    text_blank_ids = _target_text_blank_ids(target_members, slot_by_id)
    if len(text_blank_ids) == len(problem_answer_ids) and text_blank_ids:
        decorative_box_ids = {
            slot_id
            for slot_id in keep_ids
            if slot_id not in target_members
            and slot_id not in problem_answer_ids
            and slot_id not in fixed_ids
            and _slot_kind(slot_by_id.get(slot_id, {})) == "rect"
        }
        keep_ids -= decorative_box_ids

    target_left = target_box[0] if target_box is not None else None
    desired_left = _leftmost_problem_group(groups, slot_by_id)
    dx = 0.0
    if target_left is not None and desired_left is not None:
        dx = desired_left - target_left

    removed_ids = set(slot_by_id) - keep_ids

    projected_layout = copy.deepcopy(layout)
    projected_layout["slots"] = [
        slot
        for slot in projected_layout.get("slots", [])
        if isinstance(slot, dict) and slot.get("id") in keep_ids
    ]
    if abs(dx) > 0.001:
        _translate_layout_slots(
            projected_layout["slots"], dx=dx, dy=0.0, exclude_ids=fixed_ids
        )
    _align_problem_row_rest_slots(
        projected_layout["slots"],
        index=index,
        exclude_ids=protected_slot_ids,
    )
    _normalize_submit_input_rects(projected_layout["slots"])
    _convert_text_blanks_to_input_rects(
        projected_layout["slots"],
        text_blank_ids=text_blank_ids,
    )
    _expand_stem_text_boxes(projected_layout)
    projected_layout["regions"] = _project_regions(
        projected_layout.get("regions", []),
        keep_ids,
    )
    projected_layout["groups"] = [
        group
        for group in projected_layout.get("groups", [])
        if isinstance(group, dict)
        and (
            group_id is None or group.get("id") == group_id or _is_context_group(group)
        )
    ]
    if isinstance(projected_layout.get("reading_order"), list):
        projected_layout["reading_order"] = [
            item
            for item in projected_layout["reading_order"]
            if not isinstance(item, str)
            or item in keep_ids
            or item.startswith("region.")
        ]

    projected_semantic = _project_problem_payload(semantic, index)
    _project_answer_to_ids(projected_semantic.get("answer"), problem_answer_ids)
    projected_solvable = (
        _project_problem_payload(solvable, index)
        if isinstance(solvable, dict)
        else solvable
    )
    if isinstance(projected_solvable, dict):
        _project_answer_to_ids(projected_solvable.get("answer"), problem_answer_ids)
    return projected_layout, projected_semantic, projected_solvable, removed_ids


def _target_group_id(groups: list[dict[str, Any]], index: int) -> str | None:
    candidates = (f"group.problem_{index}", f"group.item_{index}")
    group_ids = {group.get("id") for group in groups}
    for candidate in candidates:
        if candidate in group_ids:
            return candidate
    return None


def _target_region_id(regions: list[dict[str, Any]], index: int) -> str | None:
    candidates = (
        f"region.problem_{index}",
        f"region.item_{index}",
        f"region.calculation.{index}",
        f"region.problem.{index}",
    )
    region_ids = {region.get("id") for region in regions}
    for candidate in candidates:
        if candidate in region_ids:
            return candidate
    return None


def _artifact_suffix_index(artifact_id: str, template_id: str | None) -> int | None:
    artifact_id = artifact_id.replace("\\", "/").rsplit("/", 1)[-1]
    if artifact_id.endswith(".dsl.py"):
        artifact_id = artifact_id[: -len(".dsl.py")]
    match = re.fullmatch(r"(.+)_([1-9]\d*)", artifact_id)
    if not match:
        return None
    base_id, raw_index = match.groups()
    if template_id and template_id not in {artifact_id, base_id}:
        return None
    return int(raw_index)


def _stem_slot_ids(layout: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for region in layout.get("regions", []):
        if not isinstance(region, dict) or region.get("role") != "stem":
            continue
        out.update(
            slot_id
            for slot_id in region.get("slot_ids", [])
            if isinstance(slot_id, str) and not _looks_like_problem_body_slot(slot_id)
        )
    return out


def _looks_like_problem_body_slot(slot_id: str) -> bool:
    return bool(
        re.search(r"(?:^|\.)calculation\.\d+(?:\.|$)", slot_id)
        or re.search(r"(?:^|\.)problem_\d+(?:\.|$)", slot_id)
        or re.search(r"(?:^|\.)item_\d+(?:\.|$)", slot_id)
    )


def _context_slot_ids(
    layout: dict[str, Any],
    groups: list[dict[str, Any]],
) -> set[str]:
    out: set[str] = set()
    for region in layout.get("regions", []):
        if not isinstance(region, dict) or not _is_context_region(region):
            continue
        out.update(
            slot_id
            for slot_id in region.get("slot_ids", [])
            if isinstance(slot_id, str)
        )
    for group in groups:
        if not _is_context_group(group):
            continue
        out.update(
            slot_id
            for slot_id in group.get("member_ids", [])
            if isinstance(slot_id, str)
        )
    return out


def _is_context_region(region: dict[str, Any]) -> bool:
    role = _lower_str(region.get("role"))
    region_id = _lower_str(region.get("id"))
    return role in _CONTEXT_REGION_ROLES or any(
        token in role or token in region_id for token in _CONTEXT_TOKENS
    )


def _is_context_group(group: dict[str, Any]) -> bool:
    role = _lower_str(group.get("role"))
    group_id = _lower_str(group.get("id"))
    return any(token in role or token in group_id for token in _CONTEXT_TOKENS)


def _lower_str(value: Any) -> str:
    return value.lower() if isinstance(value, str) else ""


def _answer_slot_ids_for_problem(answer: Any, index: int) -> set[str]:
    if not isinstance(answer, dict):
        return set()
    token = f"problem_{index}"
    out: set[str] = set()
    for key in ("blanks", "answer_key"):
        items = answer.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str):
                slot_index = _identifier_problem_index(slot_id)
                if slot_index == index or token in slot_id:
                    out.add(slot_id)
    return out


def _answer_slot_ids_for_target_members(
    target_members: set[str],
    slot_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    return {
        slot_id
        for slot_id in target_members
        if _slot_kind(slot_by_id.get(slot_id, {})) == "blank"
    }


def _all_submit_slot_ids(slots: list[dict[str, Any]]) -> set[str]:
    return {
        slot["id"]
        for slot in slots
        if isinstance(slot.get("id"), str) and _submit_slot_order(slot) is not None
    }


def _submit_slot_ids_for_index(slots: list[dict[str, Any]], index: int) -> set[str]:
    target_order = index - 1
    return {
        slot["id"]
        for slot in slots
        if isinstance(slot.get("id"), str) and _submit_slot_order(slot) == target_order
    }


def _submit_slot_order(slot: dict[str, Any]) -> int | None:
    content = slot.get("content")
    interaction = content.get("interaction") if isinstance(content, dict) else None
    if not isinstance(interaction, dict):
        return None
    if interaction.get("role") != "answer" or interaction.get("type") != "input":
        return None
    if interaction.get("include_in_submission") is False:
        return None
    order = interaction.get("order")
    if isinstance(order, int) and not isinstance(order, bool):
        return order
    if isinstance(order, str):
        try:
            return int(order.strip())
        except ValueError:
            return None
    return None


def _rebind_stray_ordered_submit_slots(
    *,
    ordered_submit_ids: set[str],
    target_members: set[str],
    target_box: tuple[float, float, float, float] | None,
    slot_by_id: dict[str, dict[str, Any]],
    answer: Any,
    index: int,
) -> set[str]:
    if not ordered_submit_ids or target_box is None:
        return set()
    source_slots = [
        slot_by_id[slot_id]
        for slot_id in sorted(
            ordered_submit_ids,
            key=lambda slot_id: _submit_slot_order(slot_by_id.get(slot_id, {})) or 0,
        )
        if isinstance(slot_by_id.get(slot_id), dict)
    ]
    if not source_slots:
        return set()
    target_refs = _answer_target_refs_for_problem(answer, index)
    if len(target_refs) > len(source_slots):
        target_refs = target_refs[: len(source_slots)]
    replacement_ids = _matching_answer_box_ids(
        target_members=target_members,
        slot_by_id=slot_by_id,
        target_refs=target_refs,
    )
    if len(replacement_ids) != len(source_slots):
        return set()
    if [s.get("id") for s in source_slots] == replacement_ids:
        return set()
    if not _submit_slots_should_rebind_to_targets(
        source_slots=source_slots,
        replacement_ids=replacement_ids,
        target_box=target_box,
        slot_by_id=slot_by_id,
    ):
        return set()

    for source_slot, replacement_id in zip(source_slots, replacement_ids, strict=True):
        replacement_slot = slot_by_id.get(replacement_id)
        if not isinstance(replacement_slot, dict):
            continue
        source_content = source_slot.get("content")
        replacement_content = replacement_slot.setdefault("content", {})
        if not isinstance(source_content, dict) or not isinstance(
            replacement_content, dict
        ):
            continue
        interaction = source_content.get("interaction")
        input_style = source_content.get("input_style")
        if isinstance(interaction, dict):
            replacement_content["interaction"] = copy.deepcopy(interaction)
        if isinstance(input_style, dict):
            replacement_content["input_style"] = copy.deepcopy(input_style)
        sanitize_answer_input_content(replacement_content)
    return set(replacement_ids)


def _submit_slots_should_rebind_to_targets(
    *,
    source_slots: list[dict[str, Any]],
    replacement_ids: list[str],
    target_box: tuple[float, float, float, float],
    slot_by_id: dict[str, dict[str, Any]],
) -> bool:
    for source_slot, replacement_id in zip(source_slots, replacement_ids, strict=True):
        source_box = _slot_box(source_slot)
        replacement_box = _slot_box(slot_by_id.get(replacement_id))
        if source_box is None:
            return False
        if not _box_center_in(source_box, target_box, margin=12.0):
            continue
        if replacement_box is not None and _box_center_in(
            source_box, replacement_box, margin=8.0
        ):
            continue
        return False
    return True


def _answer_target_refs_for_problem(answer: Any, index: int) -> list[str]:
    if not isinstance(answer, dict):
        return []
    refs: list[str] = []
    values = answer.get("values")
    if isinstance(values, list):
        for item in values:
            if not isinstance(item, dict):
                continue
            target_ref = item.get("target_ref")
            if (
                isinstance(target_ref, str)
                and _identifier_problem_index(target_ref) == index
            ):
                refs.append(target_ref)
    return refs


def _matching_answer_box_ids(
    *,
    target_members: set[str],
    slot_by_id: dict[str, dict[str, Any]],
    target_refs: list[str],
) -> list[str]:
    if not target_refs:
        return []
    matched: list[str] = []
    used: set[str] = set()
    for target_ref in target_refs:
        token = target_ref.rsplit(".", 1)[-1]
        candidate = next(
            (
                slot_id
                for slot_id in sorted(target_members)
                if slot_id not in used
                and _slot_kind(slot_by_id.get(slot_id, {})) == "rect"
                and _slot_id_matches_answer_target(slot_id, token)
            ),
            None,
        )
        if candidate is None:
            return []
        used.add(candidate)
        matched.append(candidate)
    return matched


def _slot_id_matches_answer_target(slot_id: str, token: str) -> bool:
    normalized = slot_id.lower().replace("_", ".")
    token = token.lower().replace("_", ".")
    return (
        normalized.endswith(f".box.{token}")
        or normalized.endswith(f".{token}")
        or f".box.{token}." in normalized
    )


def _target_answer_input_slot_ids(
    slots: list[dict[str, Any]],
    target_box: tuple[float, float, float, float] | None,
) -> set[str]:
    if target_box is None:
        return set()
    out: set[str] = set()
    for slot in slots:
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or not _is_answer_input_slot(slot):
            continue
        box = _slot_box(slot)
        if box is not None and _answer_input_near_target_box(box, target_box):
            out.add(slot_id)
    return out


def _is_answer_input_slot(slot: dict[str, Any]) -> bool:
    content = slot.get("content")
    interaction = content.get("interaction") if isinstance(content, dict) else None
    if not isinstance(interaction, dict):
        return False
    if interaction.get("role") != "answer" or interaction.get("type") != "input":
        return False
    return interaction.get("include_in_submission") is not False


def _answer_input_near_target_box(
    box: tuple[float, float, float, float],
    target_box: tuple[float, float, float, float],
) -> bool:
    cx = (box[0] + box[2]) / 2
    cy = (box[1] + box[3]) / 2
    target_width = max(1.0, target_box[2] - target_box[0])
    horizontal_margin = max(36.0, target_width * 0.45)
    return (
        target_box[0] - horizontal_margin <= cx <= target_box[2] + horizontal_margin
        and target_box[1] - 12.0 <= cy <= target_box[3] + 80.0
    )


def _normalize_submit_input_rects(slots: list[dict[str, Any]]) -> None:
    for slot in slots:
        content = slot.get("content")
        if not isinstance(content, dict):
            continue
        interaction = content.get("interaction")
        if not isinstance(interaction, dict):
            continue
        if interaction.get("role") != "answer" or interaction.get("type") != "input":
            continue
        sanitize_answer_input_content(content)
        width = content.get("width")
        if isinstance(width, int | float) and width >= 40:
            interaction["value_type"] = "integer"
            interaction["max_length"] = max(int(interaction.get("max_length") or 0), 4)
            interaction["auto_advance"] = False


def _slot_kind(slot: dict[str, Any]) -> str:
    kind = slot.get("kind")
    return kind if isinstance(kind, str) else ""


def _target_text_blank_ids(
    target_members: set[str],
    slot_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    out: list[tuple[float, float, str]] = []
    for slot_id in target_members:
        slot = slot_by_id.get(slot_id)
        if not isinstance(slot, dict) or _slot_kind(slot) != "text":
            continue
        content = slot.get("content")
        text = content.get("text") if isinstance(content, dict) else None
        if isinstance(text, str) and text.strip() == "□":
            x = content.get("x") if isinstance(content, dict) else None
            y = content.get("y") if isinstance(content, dict) else None
            out.append(
                (
                    float(y) if isinstance(y, int | float) else 0.0,
                    float(x) if isinstance(x, int | float) else 0.0,
                    slot_id,
                )
            )
    return [slot_id for _, _, slot_id in sorted(out)]


def _slot_box(slot: dict[str, Any] | None) -> tuple[float, float, float, float] | None:
    if not isinstance(slot, dict):
        return None
    content = slot.get("content")
    if not isinstance(content, dict):
        return None
    d = content.get("d")
    if isinstance(d, str):
        numbers = [float(item) for item in re.findall(r"-?\d+(?:\.\d+)?", d)]
        if len(numbers) >= 2:
            xs = numbers[0::2]
            ys = numbers[1::2]
            return min(xs), min(ys), max(xs), max(ys)
    if all(
        isinstance(content.get(key), int | float) for key in ("x1", "y1", "x2", "y2")
    ):
        x1 = float(content["x1"])
        y1 = float(content["y1"])
        x2 = float(content["x2"])
        y2 = float(content["y2"])
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    x = content.get("x")
    y = content.get("y")
    if not isinstance(x, int | float) or not isinstance(y, int | float):
        return None
    font_size = content.get("font_size")
    width = content.get("width")
    height = content.get("height")
    text = content.get("text")
    if not isinstance(width, int | float):
        if isinstance(text, str) and isinstance(font_size, int | float):
            width = max(float(font_size), len(text) * float(font_size) * 0.62)
        else:
            width = 0.0
    if not isinstance(height, int | float):
        height = float(font_size) if isinstance(font_size, int | float) else 0.0
    anchor = content.get("anchor")
    left = float(x)
    if anchor == "middle":
        left -= float(width) / 2
    elif anchor == "end":
        left -= float(width)
    top = float(y)
    return left, top, left + float(width), top + float(height)


def _union_box(
    boxes: list[tuple[float, float, float, float] | None],
) -> tuple[float, float, float, float] | None:
    clean = [box for box in boxes if box is not None]
    if not clean:
        return None
    return (
        min(box[0] for box in clean),
        min(box[1] for box in clean),
        max(box[2] for box in clean),
        max(box[3] for box in clean),
    )


def _leftmost_problem_group(
    groups: list[dict[str, Any]],
    slot_by_id: dict[str, dict[str, Any]],
) -> float | None:
    lefts: list[float] = []
    for group in groups:
        group_id = group.get("id")
        if not isinstance(group_id, str) or not re.fullmatch(
            r"group\.(problem|item)_\d+", group_id
        ):
            continue
        member_ids = [
            slot_id
            for slot_id in group.get("member_ids", [])
            if isinstance(slot_id, str)
        ]
        box = _union_box([_slot_box(slot_by_id.get(slot_id)) for slot_id in member_ids])
        if box is not None:
            lefts.append(box[0])
    return min(lefts) if lefts else None


def _translate_layout_slots(
    slots: list[dict[str, Any]],
    *,
    dx: float,
    dy: float,
    exclude_ids: set[str],
) -> None:
    for slot in slots:
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or slot_id in exclude_ids:
            continue
        content = slot.get("content")
        if not isinstance(content, dict):
            continue
        for key in ("x", "cx", "x1", "x2"):
            value = content.get(key)
            if isinstance(value, int | float):
                content[key] = round(float(value) + dx, 3)
        for key in ("y", "cy", "y1", "y2"):
            value = content.get(key)
            if isinstance(value, int | float):
                content[key] = round(float(value) + dy, 3)


def _convert_text_blanks_to_input_rects(
    slots: list[dict[str, Any]],
    *,
    text_blank_ids: list[str],
) -> None:
    for order, slot_id in enumerate(text_blank_ids):
        slot = next((item for item in slots if item.get("id") == slot_id), None)
        if not isinstance(slot, dict):
            continue
        content = slot.get("content")
        if not isinstance(content, dict):
            continue
        x = content.get("x")
        y = content.get("y")
        font_size = content.get("font_size")
        if not isinstance(x, int | float) or not isinstance(y, int | float):
            continue
        existing_width = content.get("width")
        existing_height = content.get("height")
        has_rect_override = isinstance(existing_width, int | float) and isinstance(
            existing_height, int | float
        )
        size = float(font_size) * 0.82 if isinstance(font_size, int | float) else 18.0
        rect_width = float(existing_width) if has_rect_override else size
        rect_height = float(existing_height) if has_rect_override else size
        rect_x = float(x) if has_rect_override else float(x) - rect_width / 2
        rect_y = float(y) if has_rect_override else float(y) - rect_height * 0.78
        slot["kind"] = "rect"
        slot["content"] = {
            "x": round(rect_x, 3),
            "y": round(rect_y, 3),
            "width": round(rect_width, 3),
            "height": round(rect_height, 3),
            "fill": "#ffffff",
            "stroke": (
                content.get("stroke")
                if isinstance(content.get("stroke"), str)
                else "#111827"
            ),
            "stroke_width": (
                content.get("stroke_width")
                if isinstance(content.get("stroke_width"), int | float)
                else 1.2
            ),
            "interaction": {
                "type": "input",
                "role": "answer",
                "include_in_submission": True,
                "order": order,
                "group_id": "final_answer",
                "answer_key_index": order,
                "answer_ref": f"answer_key[{order}]",
            },
            "input_style": {
                "width": round(rect_width, 3),
                "height": round(rect_height, 3),
                "font_size": round(min(rect_width, rect_height) * 0.72, 3),
            },
        }
        sanitize_answer_input_content(slot["content"])


def _align_problem_row_rest_slots(
    slots: list[dict[str, Any]],
    *,
    index: int,
    exclude_ids: set[str] | None = None,
) -> None:
    exclude_ids = exclude_ids or set()
    y_by_row: dict[str, float] = {}
    blank_pattern = re.compile(rf"^slot\.blank_{index}_(.+)_[^.]+$")
    rest_pattern = re.compile(rf"^slot\.number_{index}_(.+)_rest$")
    for slot in slots:
        slot_id = slot.get("id")
        if not isinstance(slot_id, str):
            continue
        match = blank_pattern.fullmatch(slot_id)
        if not match:
            continue
        content = slot.get("content")
        y = content.get("y") if isinstance(content, dict) else None
        if isinstance(y, int | float):
            y_by_row[match.group(1)] = float(y)

    for slot in slots:
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or slot_id in exclude_ids:
            continue
        match = rest_pattern.fullmatch(slot_id)
        if not match or match.group(1) not in y_by_row:
            continue
        content = slot.get("content")
        if isinstance(content, dict):
            content["y"] = round(y_by_row[match.group(1)], 3)


def _expand_stem_text_boxes(layout: dict[str, Any]) -> None:
    stem_ids = _stem_slot_ids(layout)
    if not stem_ids:
        return
    max_delta = 0.0
    for slot in layout.get("slots", []):
        if not isinstance(slot, dict) or slot.get("id") not in stem_ids:
            continue
        if slot.get("kind") != "text_box":
            continue
        content = slot.get("content")
        if not isinstance(content, dict):
            continue
        needed = _minimum_text_box_height(content)
        height = content.get("height")
        if needed is None or not isinstance(height, int | float) or needed <= height:
            continue
        max_delta = max(max_delta, needed - float(height))
        content["height"] = round(needed, 3)
    if max_delta <= 0:
        return
    _translate_layout_slots(
        layout.get("slots", []),
        dx=0.0,
        dy=max_delta,
        exclude_ids=stem_ids,
    )
    canvas = layout.get("canvas")
    if isinstance(canvas, dict) and isinstance(canvas.get("height"), int | float):
        canvas["height"] = round(float(canvas["height"]) + max_delta, 3)


def _minimum_text_box_height(content: dict[str, Any]) -> float | None:
    text = content.get("text")
    width = content.get("width")
    font_size = content.get("font_size")
    if not isinstance(text, str) or not text:
        return None
    if not isinstance(width, int | float) or width <= 0:
        return None
    if not isinstance(font_size, int | float) or font_size <= 0:
        return None
    line_height = content.get("line_height")
    if not isinstance(line_height, int | float) or line_height <= 0:
        line_height = 1.25
    usable_width = max(float(font_size), float(width))
    line_count = sum(
        max(
            1,
            int(
                (_text_width(line, float(font_size)) + usable_width - 1) // usable_width
            ),
        )
        for line in text.splitlines() or [""]
    )
    return max(24.0, line_count * float(font_size) * float(line_height) + 8.0)


def _text_width(text: str, font_size: float) -> float:
    width = 0.0
    for char in text:
        if char.isspace():
            width += font_size * 0.34
        elif (
            "\u1100" <= char <= "\u11ff"
            or "\u3130" <= char <= "\u318f"
            or "\uac00" <= char <= "\ud7af"
            or "\u3400" <= char <= "\u9fff"
        ):
            width += font_size
        elif char.isupper() or char.isdigit():
            width += font_size * 0.62
        elif char.islower():
            width += font_size * 0.54
        else:
            width += font_size * 0.5
    return width


def _box_center_in(
    box: tuple[float, float, float, float],
    container: tuple[float, float, float, float],
    *,
    margin: float,
) -> bool:
    cx = (box[0] + box[2]) / 2
    cy = (box[1] + box[3]) / 2
    return (
        container[0] - margin <= cx <= container[2] + margin
        and container[1] - margin <= cy <= container[3] + margin
    )


def _project_regions(regions: Any, keep_ids: set[str]) -> list[dict[str, Any]]:
    projected: list[dict[str, Any]] = []
    if not isinstance(regions, list):
        return projected
    for region in regions:
        if not isinstance(region, dict):
            continue
        kept = [
            slot_id
            for slot_id in region.get("slot_ids", [])
            if isinstance(slot_id, str) and slot_id in keep_ids
        ]
        if not kept and region.get("role") != "stem":
            continue
        next_region = dict(region)
        next_region["slot_ids"] = kept
        projected.append(next_region)
    return projected


def _project_problem_payload(payload: dict[str, Any], index: int) -> dict[str, Any]:
    projected = copy.deepcopy(payload)
    token = f"problem_{index}"
    for key in ("domain", "given", "understanding", "steps", "checks", "answer"):
        if key in projected:
            projected[key] = _filter_problem_refs(projected[key], token)
    if isinstance(projected.get("answer"), dict):
        _sync_answer_values(projected["answer"])
    return projected


def _sync_answer_values(answer: dict[str, Any]) -> None:
    values: list[Any] = []
    answer_key = answer.get("answer_key")
    if isinstance(answer_key, list):
        for item in answer_key:
            if isinstance(item, dict) and "value" in item:
                values.append(item["value"])
    if not values:
        blanks = answer.get("blanks")
        if isinstance(blanks, list):
            for item in blanks:
                if not isinstance(item, dict):
                    continue
                if "value" in item:
                    values.append(item["value"])
                elif "expected" in item:
                    values.append(item["expected"])
    if not values:
        answer_values = answer.get("values")
        if isinstance(answer_values, list):
            for item in answer_values:
                if isinstance(item, dict) and "value" in item:
                    values.append(item["value"])
                elif isinstance(item, str | int | float) and not isinstance(item, bool):
                    values.append(item)
    if values and isinstance(answer.get("value"), list):
        answer["value"] = values
    if (
        values
        and isinstance(answer.get("values"), list)
        and not all(isinstance(item, dict) for item in answer["values"])
    ):
        answer["values"] = values


def _project_answer_to_ids(answer: Any, keep_ids: set[str]) -> None:
    if not isinstance(answer, dict) or not keep_ids:
        return
    values: list[Any] = []
    for key in ("blanks", "answer_key"):
        items = answer.get(key)
        if not isinstance(items, list):
            continue
        kept_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id in keep_ids:
                kept_items.append(item)
                if key == "answer_key" and "value" in item:
                    values.append(item["value"])
        answer[key] = kept_items
    if not values:
        for item in answer.get("blanks", []):
            if isinstance(item, dict):
                if "value" in item:
                    values.append(item["value"])
                elif "expected" in item:
                    values.append(item["expected"])
    if values and isinstance(answer.get("value"), list):
        answer["value"] = values
    if values and isinstance(answer.get("values"), list):
        answer["values"] = values


def _filter_problem_refs(value: Any, token: str) -> Any:
    if isinstance(value, list):
        filtered = []
        for item in value:
            if _mentions_other_problem(item, token):
                continue
            next_item = _filter_problem_refs(item, token)
            if next_item is not _DROP:
                filtered.append(next_item)
        return filtered
    if isinstance(value, dict):
        if _dict_mentions_other_problem(value, token):
            return _DROP
        return {
            key: filtered
            for key, item in value.items()
            if (filtered := _filter_problem_refs(item, token)) is not _DROP
        }
    return value


def _dict_mentions_other_problem(value: dict[str, Any], token: str) -> bool:
    target_index = _token_index(token)
    if target_index is None:
        return False
    identifiers = []
    for key in (
        "id",
        "ref",
        "blank_id",
        "slot_id",
        "target_ref",
        "result",
        "subject",
        "object",
    ):
        raw = value.get(key)
        if isinstance(raw, str):
            identifiers.append(raw)
    for identifier in identifiers:
        index = _identifier_problem_index(identifier)
        if index is not None and index != target_index:
            return True
    return False


def _token_index(token: str) -> int | None:
    match = re.fullmatch(r"problem_(\d+)", token)
    return int(match.group(1)) if match else None


def _identifier_problem_index(identifier: str) -> int | None:
    patterns = (
        r"(?:^|[._])problem_(\d+)(?:[._]|$)",
        r"(?:^|\.)answer\.(\d+)(?:\.|$)",
        r"(?:^|\.)calculation\.(\d+)(?:\.|$)",
        r"(?:^|\.)item\.(\d+)(?:\.|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, identifier)
        if match:
            return int(match.group(1))
    return None


def _mentions_other_problem(value: Any, token: str) -> bool:
    if isinstance(value, dict):
        if _dict_mentions_other_problem(value, token):
            return True
        return any(_mentions_other_problem(item, token) for item in value.values())
    if isinstance(value, list):
        return any(_mentions_other_problem(item, token) for item in value)
    return False


class _Drop:
    pass


_DROP = _Drop()
