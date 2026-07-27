from __future__ import annotations

import re
from typing import Any


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


def _infer_region_id_for_slot(layout: dict[str, Any], slot_id: str) -> str | None:
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
    region_ids = [
        region.get("id")
        for region in layout.get("regions", [])
        if isinstance(region, dict) and isinstance(region.get("id"), str)
    ]
    if len(region_ids) == 1:
        return region_ids[0]
    return None


def _add_missing_override_slot(layout: dict[str, Any], slot_id: str, content: dict[str, Any]) -> None:
    region_id = _infer_region_id_for_slot(layout, slot_id)
    if region_id is None:
        return

    slots = layout.setdefault("slots", [])
    if not isinstance(slots, list):
        layout["slots"] = []
        slots = layout["slots"]
    slots.append({"id": slot_id, "kind": _infer_override_slot_kind(content), "prompt": "", "content": dict(content)})

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


def prune_editor_overrides(layout: dict[str, Any], overrides: dict[str, Any] | None) -> tuple[dict[str, Any] | None, bool]:
    if not isinstance(overrides, dict):
        return overrides, False

    changed = False
    cleaned: dict[str, Any] = {key: value for key, value in overrides.items() if key not in {"slots", "region_slot_orders"}}
    slot_ids = _layout_slot_ids(layout)
    slot_kinds = _layout_slot_kinds(layout)

    retained_override_slot_ids: set[str] = set()
    slot_overrides = overrides.get("slots")
    if isinstance(slot_overrides, dict):
        cleaned_slots: dict[str, Any] = {}
        for slot_id, patch in slot_overrides.items():
            if not isinstance(slot_id, str) or not isinstance(patch, dict):
                changed = True
                continue
            if slot_id in slot_ids or _infer_region_id_for_slot(layout, slot_id) is not None:
                patch, normalized = _normalize_slot_patch(slot_kinds.get(slot_id), patch)
                changed = changed or normalized
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

        slots = layout.get("slots")
        if isinstance(slots, list):
            layout["slots"] = [slot for slot in slots if not (isinstance(slot, dict) and is_deleted(slot.get("id")))]
        for region in layout.get("regions", []):
            if isinstance(region, dict) and isinstance(region.get("slot_ids"), list):
                region["slot_ids"] = [slot_id for slot_id in region["slot_ids"] if not is_deleted(slot_id)]
        if isinstance(layout.get("reading_order"), list):
            layout["reading_order"] = [item for item in layout["reading_order"] if not is_deleted(item)]

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

    canvas_override = overrides.get("canvas")
    canvas = layout.get("canvas")
    if isinstance(canvas, dict) and isinstance(canvas_override, dict):
        canvas.update(canvas_override)

    return layout
