from __future__ import annotations

from typing import Any


def apply_editor_overrides(layout: dict[str, Any], overrides: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(overrides, dict):
        return layout

    deleted_slots = overrides.get("deleted_slots")
    deleted = {slot_id for slot_id in deleted_slots if isinstance(slot_id, str)} if isinstance(deleted_slots, list) else set()
    if deleted:
        slots = layout.get("slots")
        if isinstance(slots, list):
            layout["slots"] = [slot for slot in slots if not (isinstance(slot, dict) and slot.get("id") in deleted)]
        for region in layout.get("regions", []):
            if isinstance(region, dict) and isinstance(region.get("slot_ids"), list):
                region["slot_ids"] = [slot_id for slot_id in region["slot_ids"] if slot_id not in deleted]
        if isinstance(layout.get("reading_order"), list):
            layout["reading_order"] = [item for item in layout["reading_order"] if item not in deleted]

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
