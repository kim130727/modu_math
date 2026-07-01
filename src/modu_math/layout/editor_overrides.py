from __future__ import annotations

from typing import Any


def _infer_override_slot_kind(content: dict[str, Any]) -> str:
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
    if best_region_id:
        return best_region_id
    for region in layout.get("regions", []):
        if isinstance(region, dict) and region.get("role") == "diagram" and isinstance(region.get("id"), str):
            return region["id"]
    for region in layout.get("regions", []):
        if isinstance(region, dict) and isinstance(region.get("id"), str):
            return region["id"]
    return None


def _add_missing_override_slot(layout: dict[str, Any], slot_id: str, content: dict[str, Any]) -> None:
    slots = layout.setdefault("slots", [])
    if not isinstance(slots, list):
        layout["slots"] = []
        slots = layout["slots"]
    slots.append({"id": slot_id, "kind": _infer_override_slot_kind(content), "prompt": "", "content": dict(content)})

    region_id = _infer_region_id_for_slot(layout, slot_id)
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
                content.update(patch)

    canvas_override = overrides.get("canvas")
    canvas = layout.get("canvas")
    if isinstance(canvas, dict) and isinstance(canvas_override, dict):
        canvas.update(canvas_override)

    return layout
