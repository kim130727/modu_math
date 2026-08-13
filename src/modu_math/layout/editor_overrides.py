from __future__ import annotations

import re
from typing import Any


def _text_width(text: str, font_size: float) -> float:
    width = 0.0
    for char in text:
        if char.isspace():
            width += font_size * 0.34
        elif "\u1100" <= char <= "\u11ff" or "\u3130" <= char <= "\u318f" or "\uac00" <= char <= "\ud7af" or "\u3400" <= char <= "\u9fff":
            width += font_size
        elif char.isupper() or char.isdigit():
            width += font_size * 0.62
        elif char.islower():
            width += font_size * 0.54
        else:
            width += font_size * 0.5
    return width


def _minimum_text_box_height(content: dict[str, Any], patch: dict[str, Any] | None = None) -> float | None:
    merged = dict(content)
    if patch:
        merged.update(patch)
    text = merged.get("text")
    width = merged.get("width")
    font_size = merged.get("font_size")
    if not isinstance(text, str) or not text:
        return None
    if not isinstance(width, int | float) or width <= 0:
        return None
    if not isinstance(font_size, int | float) or font_size <= 0:
        return None
    line_height = merged.get("line_height")
    if not isinstance(line_height, int | float) or line_height <= 0:
        line_height = 1.25
    usable_width = max(float(font_size), float(width))
    line_count = sum(max(1, int((_text_width(line, float(font_size)) + usable_width - 1) // usable_width)) for line in text.splitlines() or [""])
    return max(24.0, line_count * float(font_size) * float(line_height) + 8.0)


def _normalize_text_box_height(content: dict[str, Any], patch: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    if "height" not in patch:
        return patch, False
    height = patch.get("height")
    if not isinstance(height, int | float):
        return patch, False
    minimum = _minimum_text_box_height(content, patch)
    base_height = content.get("height")
    if isinstance(base_height, int | float):
        minimum = max(float(base_height), minimum or 0.0)
    if minimum is None or height >= minimum:
        return patch, False
    normalized = dict(patch)
    normalized["height"] = round(minimum, 3)
    return normalized, True


def _normalize_answer_input_interaction(content: dict[str, Any]) -> None:
    interaction = content.get("interaction")
    if not isinstance(interaction, dict):
        return
    width = content.get("width")
    if (
        interaction.get("type") == "input"
        and interaction.get("role") == "answer"
        and interaction.get("value_type") == "digit"
        and interaction.get("max_length") == 1
        and isinstance(width, int | float)
        and width >= 60
    ):
        interaction["value_type"] = "integer"
        interaction["max_length"] = 3
        interaction["auto_advance"] = False


def _is_answer_slot_id(slot_id: str) -> bool:
    return slot_id == "slot.answer" or slot_id.endswith(".answer") or ".answer." in slot_id


def _layout_has_answer_interaction(layout: dict[str, Any], deleted: set[str]) -> bool:
    for slot in layout.get("slots", []):
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or _deleted_slot_matches(slot_id, deleted, deleted & _layout_slot_ids(layout)):
            continue
        content = slot.get("content")
        interaction = content.get("interaction") if isinstance(content, dict) else None
        if isinstance(interaction, dict) and interaction.get("role") == "answer":
            return True
    return False


def _infer_override_slot_kind(content: dict[str, Any]) -> str:
    if "d" in content:
        return "path"
    if (
        "width" in content
        or "height" in content
        or "align" in content
        or "valign" in content
        or "line_height" in content
    ) and ("text" in content or "font_size" in content):
        return "text_box"
    if "text" in content or "font_size" in content or "max_width" in content:
        return "text"
    if "x1" in content or "y1" in content or "x2" in content or "y2" in content:
        return "line"
    if "cx" in content or "cy" in content or "r" in content:
        return "circle"
    if "href" in content or "src" in content:
        return "image"
    return "rect"


def _slot_prefix_score(slot_id: str, candidate: str) -> int:
    slot_parts = slot_id.split(".")
    candidate_parts = candidate.split(".")
    score = 0
    for left, right in zip(slot_parts, candidate_parts):
        if left != right:
            break
        score += 1
    return score


def _override_is_answer_slot(slot_id: str, content: dict[str, Any]) -> bool:
    interaction = content.get("interaction")
    return (
        (isinstance(interaction, dict) and interaction.get("role") == "answer")
        or slot_id.startswith("answer.")
        or ".answer" in slot_id
    )


def _infer_region_id_for_slot(layout: dict[str, Any], slot_id: str, content: dict[str, Any] | None = None) -> str | None:
    best_region_id: str | None = None
    best_score = 0
    for region in layout.get("regions", []):
        if not isinstance(region, dict) or not isinstance(region.get("slot_ids"), list):
            continue
        for existing_id in region["slot_ids"]:
            if not isinstance(existing_id, str):
                continue
            score = _slot_prefix_score(slot_id, existing_id)
            if score > best_score:
                best_score = score
                best_region_id = region.get("id") if isinstance(region.get("id"), str) else None
    if best_region_id and best_score >= 2:
        return best_region_id
    if content is not None and _override_is_answer_slot(slot_id, content):
        region_ids = [
            region.get("id")
            for region in layout.get("regions", [])
            if isinstance(region, dict) and isinstance(region.get("id"), str)
        ]
        if len(region_ids) == 1:
            return region_ids[0]
    return None


def _add_missing_override_slot(layout: dict[str, Any], slot_id: str, content: dict[str, Any]) -> None:
    region_id = _infer_region_id_for_slot(layout, slot_id, content)
    if region_id is None:
        return

    slots = layout.setdefault("slots", [])
    if not isinstance(slots, list):
        layout["slots"] = []
        slots = layout["slots"]
    normalized_content = dict(content)
    _normalize_answer_input_interaction(normalized_content)
    slots.append({"id": slot_id, "kind": _infer_override_slot_kind(content), "prompt": "", "content": normalized_content})

    for region in layout.get("regions", []):
        if not isinstance(region, dict) or region.get("id") != region_id:
            continue
        slot_ids = region.setdefault("slot_ids", [])
        if isinstance(slot_ids, list) and slot_id not in slot_ids:
            slot_ids.append(slot_id)
        break

    reading_order = layout.get("reading_order")
    if isinstance(reading_order, list) and slot_id not in reading_order:
        reading_order.append(slot_id)


def _deleted_slot_matches(slot_id: str, deleted: set[str], exact_deleted: set[str]) -> bool:
    if slot_id in deleted:
        return True
    for deleted_id in deleted - exact_deleted:
        if slot_id.startswith(f"{deleted_id}."):
            return True
    return False


def _layout_slot_ids(layout: dict[str, Any]) -> set[str]:
    return {
        slot.get("id")
        for slot in layout.get("slots", [])
        if isinstance(slot, dict) and isinstance(slot.get("id"), str)
    }


def _layout_slot_kinds(layout: dict[str, Any]) -> dict[str, str]:
    return {
        slot["id"]: slot["kind"]
        for slot in layout.get("slots", [])
        if isinstance(slot, dict) and isinstance(slot.get("id"), str) and isinstance(slot.get("kind"), str)
    }


def _answer_slot_ids(answer: Any) -> set[str]:
    if not isinstance(answer, dict):
        return set()
    out: set[str] = set()
    for key in ("blanks", "answer_key"):
        items = answer.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id.strip():
                out.add(slot_id)
    return out


def _answer_scalar_value(answer: Any) -> Any:
    if not isinstance(answer, dict):
        return None
    value = answer.get("value")
    if isinstance(value, str | int | float) and not isinstance(value, bool):
        return value
    return None


def _submitted_answer_slot_ids(layout: dict[str, Any], deleted: set[str] | None = None) -> set[str]:
    deleted = deleted or set()
    exact_deleted = deleted & _layout_slot_ids(layout)
    out: set[str] = set()
    for slot in layout.get("slots", []):
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or _deleted_slot_matches(slot_id, deleted, exact_deleted):
            continue
        content = slot.get("content")
        interaction = content.get("interaction") if isinstance(content, dict) else None
        if (
            isinstance(interaction, dict)
            and interaction.get("role") == "answer"
            and interaction.get("type") == "input"
            and interaction.get("include_in_submission") is not False
        ):
            out.add(slot_id)
    return out


def _remove_slot_ids_from_layout(layout: dict[str, Any], remove_ids: set[str]) -> None:
    if not remove_ids:
        return
    slots = layout.get("slots")
    if isinstance(slots, list):
        layout["slots"] = [
            slot
            for slot in slots
            if not (isinstance(slot, dict) and isinstance(slot.get("id"), str) and slot["id"] in remove_ids)
        ]
    for region in layout.get("regions", []):
        if isinstance(region, dict) and isinstance(region.get("slot_ids"), list):
            region["slot_ids"] = [slot_id for slot_id in region["slot_ids"] if slot_id not in remove_ids]
    if isinstance(layout.get("reading_order"), list):
        layout["reading_order"] = [slot_id for slot_id in layout["reading_order"] if slot_id not in remove_ids]


def prune_legacy_answer_blank_slots(layout: dict[str, Any], answer: Any) -> tuple[dict[str, Any], set[str]]:
    """Remove old BlankSlot answers when a visual input slot now owns submission.

    Older DSL files often kept a `slot.answer` BlankSlot for the semantic answer
    while editors added a positioned RectSlot with `interaction`. Rendering both
    creates a duplicate answer box. If exactly one visual answer input is present,
    answer-like blank slots are legacy scaffolding and should not render.
    """
    if _answer_scalar_value(answer) is None or len(_submitted_answer_slot_ids(layout)) != 1:
        return layout, set()

    answer_slot_ids = _answer_slot_ids(answer)
    remove_ids = {
        slot.get("id")
        for slot in layout.get("slots", [])
        if (
            isinstance(slot, dict)
            and slot.get("kind") == "blank"
            and isinstance(slot.get("id"), str)
            and (_is_answer_slot_id(slot["id"]) or slot["id"] in answer_slot_ids)
        )
    }
    remove_ids = {slot_id for slot_id in remove_ids if isinstance(slot_id, str)}
    _remove_slot_ids_from_layout(layout, remove_ids)
    return layout, remove_ids


def prune_deleted_legacy_answer_slots(
    layout: dict[str, Any],
    overrides: dict[str, Any] | None,
    answer: Any,
) -> tuple[dict[str, Any] | None, bool]:
    if not isinstance(overrides, dict):
        return overrides, False
    deleted_slots = overrides.get("deleted_slots")
    if not isinstance(deleted_slots, list):
        return overrides, False

    answer_slot_ids = _answer_slot_ids(answer)
    has_single_visual_answer = _answer_scalar_value(answer) is not None and len(_submitted_answer_slot_ids(layout, set(deleted_slots))) == 1
    if not answer_slot_ids and not has_single_visual_answer:
        return overrides, False

    slot_kinds = _layout_slot_kinds(layout)
    cleaned_deleted = [
        slot_id
        for slot_id in deleted_slots
        if not (
            isinstance(slot_id, str)
            and slot_kinds.get(slot_id) == "blank"
            and (slot_id in answer_slot_ids or has_single_visual_answer)
        )
    ]
    if cleaned_deleted == deleted_slots:
        return overrides, False

    cleaned = dict(overrides)
    if cleaned_deleted:
        cleaned["deleted_slots"] = cleaned_deleted
    else:
        cleaned.pop("deleted_slots", None)
    cleaned["version"] = 1
    return cleaned, True


def _points_from_polygon_path(d: Any) -> list[list[float]] | None:
    if not isinstance(d, str) or not d.strip():
        return None
    commands = set(re.findall(r"[A-Za-z]", d))
    if commands - {"M", "m", "L", "l", "Z", "z"}:
        return None
    numbers = [float(match.group(0)) for match in re.finditer(r"[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?", d)]
    if len(numbers) < 6 or len(numbers) % 2:
        return None
    return [[numbers[index], numbers[index + 1]] for index in range(0, len(numbers), 2)]


def _normalize_slot_patch(slot_kind: str | None, patch: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    if slot_kind != "polygon" or "d" not in patch:
        return patch, False
    normalized = dict(patch)
    points = _points_from_polygon_path(normalized.pop("d"))
    if points is not None and "points" not in normalized:
        normalized["points"] = points
    return normalized, normalized != patch


def _compact_text_for_spacing_compare(text: str) -> str:
    return "".join(char for char in text if not char.isspace())


def _whitespace_count(text: str) -> int:
    return sum(1 for char in text if char.isspace())


def _drop_stale_text_override_if_base_has_more_spacing(content: dict[str, Any], patch: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    base_text = content.get("text")
    patch_text = patch.get("text")
    if not isinstance(base_text, str) or not isinstance(patch_text, str) or base_text == patch_text:
        return patch, False
    if _compact_text_for_spacing_compare(base_text) != _compact_text_for_spacing_compare(patch_text):
        return patch, False
    if _whitespace_count(base_text) <= _whitespace_count(patch_text):
        return patch, False
    normalized = dict(patch)
    normalized.pop("text", None)
    return normalized, True


def prune_editor_overrides(layout: dict[str, Any], overrides: dict[str, Any] | None) -> tuple[dict[str, Any] | None, bool]:
    if not isinstance(overrides, dict):
        return overrides, False

    changed = False
    cleaned: dict[str, Any] = {key: value for key, value in overrides.items() if key not in {"slots", "region_slot_orders", "deleted_slots"}}
    slot_ids = _layout_slot_ids(layout)
    slot_kinds = _layout_slot_kinds(layout)
    deleted_slots = overrides.get("deleted_slots")
    if isinstance(deleted_slots, list):
        cleaned_deleted = list(deleted_slots)
        if cleaned_deleted:
            cleaned["deleted_slots"] = cleaned_deleted
        elif deleted_slots:
            changed = True

    retained_override_slot_ids: set[str] = set()
    slot_overrides = overrides.get("slots")
    if isinstance(slot_overrides, dict):
        cleaned_slots: dict[str, Any] = {}
        for slot_id, patch in slot_overrides.items():
            if not isinstance(slot_id, str) or not isinstance(patch, dict):
                changed = True
                continue
            if slot_id in slot_ids or _infer_region_id_for_slot(layout, slot_id, patch) is not None:
                patch, normalized = _normalize_slot_patch(slot_kinds.get(slot_id), patch)
                base_slot = next((slot for slot in layout.get("slots", []) if isinstance(slot, dict) and slot.get("id") == slot_id), None)
                base_content = base_slot.get("content") if isinstance(base_slot, dict) and isinstance(base_slot.get("content"), dict) else {}
                patch, text_spacing_normalized = _drop_stale_text_override_if_base_has_more_spacing(base_content, patch)
                normalized = normalized or text_spacing_normalized
                if slot_kinds.get(slot_id) == "text_box":
                    patch, text_normalized = _normalize_text_box_height(base_content, patch)
                    normalized = normalized or text_normalized
                changed = changed or normalized
                if patch:
                    cleaned_slots[slot_id] = patch
                    retained_override_slot_ids.add(slot_id)
            else:
                changed = True
        if cleaned_slots:
            cleaned["slots"] = cleaned_slots
        elif slot_overrides:
            changed = True

    region_slot_orders = overrides.get("region_slot_orders")
    if isinstance(region_slot_orders, dict):
        valid_order_ids = slot_ids | retained_override_slot_ids
        cleaned_orders: dict[str, list[str]] = {}
        for region_id, order in region_slot_orders.items():
            if not isinstance(region_id, str) or not isinstance(order, list):
                changed = True
                continue
            cleaned_order = [slot_id for slot_id in order if isinstance(slot_id, str) and slot_id in valid_order_ids]
            if cleaned_order != order:
                changed = True
            if cleaned_order:
                cleaned_orders[region_id] = cleaned_order
        if cleaned_orders:
            cleaned["region_slot_orders"] = cleaned_orders
        elif region_slot_orders:
            changed = True

    if changed:
        cleaned["version"] = 1
    elif cleaned != overrides:
        changed = True

    return cleaned, changed


def apply_editor_overrides(layout: dict[str, Any], overrides: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(overrides, dict):
        return layout

    deleted_slots = overrides.get("deleted_slots")
    deleted = {slot_id for slot_id in deleted_slots if isinstance(slot_id, str)} if isinstance(deleted_slots, list) else set()
    if deleted:
        slot_ids = {
            slot.get("id")
            for slot in layout.get("slots", [])
            if isinstance(slot, dict) and isinstance(slot.get("id"), str)
        }
        exact_deleted = deleted & slot_ids

        def is_deleted(slot_id: Any) -> bool:
            return isinstance(slot_id, str) and _deleted_slot_matches(slot_id, deleted, exact_deleted)

        remove_ids = {slot_id for slot_id in slot_ids if is_deleted(slot_id)}
        _remove_slot_ids_from_layout(layout, remove_ids)

    region_slot_orders = overrides.get("region_slot_orders")
    if isinstance(region_slot_orders, dict):
        for region in layout.get("regions", []):
            if not isinstance(region, dict):
                continue
            region_id = region.get("id")
            override_order = region_slot_orders.get(region_id) if isinstance(region_id, str) else None
            current_order = region.get("slot_ids")
            if not isinstance(override_order, list) or not isinstance(current_order, list):
                continue
            current_set = {slot_id for slot_id in current_order if isinstance(slot_id, str)}
            ordered = [slot_id for slot_id in override_order if isinstance(slot_id, str) and slot_id in current_set]
            ordered.extend(slot_id for slot_id in current_order if isinstance(slot_id, str) and slot_id not in ordered)
            region["slot_ids"] = ordered

    slot_overrides = overrides.get("slots")
    if isinstance(slot_overrides, dict):
        slot_ids = {
            slot.get("id")
            for slot in layout.get("slots", [])
            if isinstance(slot, dict) and isinstance(slot.get("id"), str)
        }
        for slot_id, patch in slot_overrides.items():
            if (
                isinstance(slot_id, str)
                and slot_id
                and slot_id not in slot_ids
                and isinstance(patch, dict)
                and not _deleted_slot_matches(slot_id, deleted, deleted & slot_ids)
            ):
                _add_missing_override_slot(layout, slot_id, patch)
                slot_ids.add(slot_id)

        for slot in layout.get("slots", []):
            if not isinstance(slot, dict):
                continue
            slot_id = slot.get("id")
            patch = slot_overrides.get(slot_id) if isinstance(slot_id, str) else None
            if not isinstance(patch, dict):
                continue
            content = slot.get("content")
            if isinstance(content, dict):
                patch, _ = _normalize_slot_patch(slot.get("kind") if isinstance(slot.get("kind"), str) else None, patch)
                content.update(patch)
                _normalize_answer_input_interaction(content)

    canvas_override = overrides.get("canvas")
    canvas = layout.get("canvas")
    if isinstance(canvas, dict) and isinstance(canvas_override, dict):
        canvas.update(canvas_override)

    return layout
