from __future__ import annotations

import re
from typing import Any


class AnswerContractError(ValueError):
    pass


def normalize_answer_for_deleted_slots(
    answer: Any, deleted_slots: set[str] | None
) -> tuple[Any, set[str]]:
    """Drop answer entries that reference editor-deleted layout slots.

    Splitting a multi-part problem in the editor can intentionally delete one of
    several visual answer blanks while the DSL-level semantic/solvable answer
    still contains the full original answer list. Keep the remaining entries in
    sync so contract validation catches real mismatches instead of stale deletes.
    """
    if not isinstance(answer, dict) or not deleted_slots:
        return answer, set()

    normalized = dict(answer)
    removed_ids: set[str] = set()
    kept_answer_values: list[Any] = []

    for key, value_key in (("blanks", "expected"), ("answer_key", "value")):
        items = normalized.get(key)
        if not isinstance(items, list):
            continue
        kept_items: list[Any] = []
        removed_any = False
        for item in items:
            if not isinstance(item, dict):
                kept_items.append(item)
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and _deleted_slot_matches(
                slot_id, deleted_slots
            ):
                removed_ids.add(slot_id)
                removed_any = True
                continue
            kept_items.append(item)
            if key == "answer_key" and value_key in item:
                kept_answer_values.append(item[value_key])
        if removed_any:
            normalized[key] = kept_items

    if not removed_ids:
        return answer, set()

    if kept_answer_values and isinstance(normalized.get("value"), list):
        normalized["value"] = list(kept_answer_values)
    if kept_answer_values and isinstance(normalized.get("values"), list):
        normalized["values"] = list(kept_answer_values)

    return normalized, removed_ids


def normalize_answer_for_submit_slots(
    answer: Any, submit_slot_ids: list[Any] | tuple[Any, ...]
) -> tuple[Any, bool]:
    """Point answer entries at the actual submitted input slots when counts align.

    Editor copies often keep the DSL's logical BlankSlot IDs in semantic/solvable
    while the copied visual RectSlots become the submitted input slots. When the
    answer values line up one-for-one with those submit slots, the visual slots
    are the authoritative submission contract.
    """
    if not isinstance(answer, dict) or not submit_slot_ids:
        return answer, False

    answer, unit_normalized = normalize_answer_value_units(answer)
    submit_slots = [_submit_slot_descriptor(slot) for slot in submit_slot_ids]
    submit_slots = [slot for slot in submit_slots if slot["slot_id"]]
    clean_submit_ids = [slot["slot_id"] for slot in submit_slots]
    if not clean_submit_ids:
        return answer, unit_normalized

    if _answer_slot_ids(answer) == set(clean_submit_ids):
        return answer, unit_normalized

    values = _answer_values_for_submit_slots(answer, submit_slots)
    if len(values) != len(clean_submit_ids):
        return answer, False

    normalized = dict(answer)
    unit = answer.get("unit")
    blanks: list[dict[str, Any]] = []
    answer_key: list[dict[str, Any]] = []
    for slot_id, value in zip(clean_submit_ids, values, strict=True):
        blank = {"id": slot_id, "slot_id": slot_id, "expected": value}
        key = {"slot_id": slot_id, "value": value}
        if isinstance(unit, str):
            blank["unit"] = unit
            key["unit"] = unit
        blanks.append(blank)
        answer_key.append(key)

    normalized["blanks"] = blanks
    normalized["answer_key"] = answer_key
    if isinstance(answer.get("value"), list):
        normalized["value"] = list(values)
    if isinstance(answer.get("values"), list):
        normalized["values"] = list(values)
    return normalized, True


def normalize_answer_value_units(answer: Any) -> tuple[Any, bool]:
    """Keep numeric answer values unit-free while preserving answer.unit."""
    if not isinstance(answer, dict):
        return answer, False
    unit = answer.get("unit")
    if not isinstance(unit, str) or not unit.strip():
        return answer, False

    changed = False
    normalized = dict(answer)

    if "value" in normalized:
        value, value_changed = _strip_unit_from_answer_value(normalized["value"], unit)
        if value_changed:
            normalized["value"] = value
            changed = True

    for key, value_key in (
        ("values", "value"),
        ("blanks", "expected"),
        ("answer_key", "value"),
    ):
        items = normalized.get(key)
        if not isinstance(items, list):
            continue
        normalized_items: list[Any] = []
        items_changed = False
        for item in items:
            if isinstance(item, dict) and value_key in item:
                item_value, item_changed = _strip_unit_from_answer_value(
                    item[value_key], unit
                )
                if item_changed:
                    normalized_item = dict(item)
                    normalized_item[value_key] = item_value
                    normalized_items.append(normalized_item)
                    items_changed = True
                    continue
            normalized_items.append(item)
        if items_changed:
            normalized[key] = normalized_items
            changed = True

    return (normalized, True) if changed else (answer, False)


def _strip_unit_from_answer_value(value: Any, unit: str) -> tuple[Any, bool]:
    if not isinstance(value, str):
        return value, False
    text = value.strip()
    unit_text = unit.strip()
    if not text or not unit_text:
        return value, False
    match = re.fullmatch(rf"([+-]?\d+(?:\.\d+)?)\s*{re.escape(unit_text)}", text)
    if not match:
        return value, False
    number_text = match.group(1)
    if "." in number_text:
        return float(number_text), True
    return int(number_text), True


def _submit_slot_descriptor(slot: Any) -> dict[str, Any]:
    if isinstance(slot, str):
        return {
            "slot_id": slot,
            "answer_key_index": None,
            "answer_ref": None,
            "order": None,
        }
    if not isinstance(slot, dict):
        return {
            "slot_id": "",
            "answer_key_index": None,
            "answer_ref": None,
            "order": None,
        }
    slot_id = slot.get("slot_id") or slot.get("id")
    return {
        "slot_id": slot_id if isinstance(slot_id, str) else "",
        "answer_key_index": slot.get("answer_key_index"),
        "answer_ref": slot.get("answer_ref"),
        "order": slot.get("order"),
    }


def validate_answer_slot_contract(
    *,
    layout: dict[str, Any],
    semantic: dict[str, Any],
    solvable: dict[str, Any] | None = None,
    deleted_slots: set[str] | None = None,
) -> None:
    """Validate that answer payloads point at the actual submitted layout slots.

    Authoring often has visual blanks, generated Konva input rectangles, and editor
    overrides in play at the same time. This check prevents stale answer slots from
    surviving in semantic/solvable after the visual layout has moved on.
    """
    deleted_slots = deleted_slots or set()
    layout_slot_ids = _layout_slot_ids(layout)
    submit_slot_ids = _submitted_answer_slot_ids(layout)
    semantic_answer_ids = _answer_slot_ids(semantic.get("answer"))

    _assert_answer_ids_exist(
        label="semantic.answer",
        answer_ids=semantic_answer_ids,
        layout_slot_ids=layout_slot_ids,
        deleted_slots=deleted_slots,
    )
    _assert_answer_ids_match_submit_slots(
        label="semantic.answer",
        answer_ids=semantic_answer_ids,
        submit_slot_ids=submit_slot_ids,
    )

    if solvable is not None:
        solvable_answer_ids = _answer_slot_ids(solvable.get("answer"))
        _assert_answer_ids_exist(
            label="solvable.answer",
            answer_ids=solvable_answer_ids,
            layout_slot_ids=layout_slot_ids,
            deleted_slots=deleted_slots,
        )
        _assert_answer_ids_match_submit_slots(
            label="solvable.answer",
            answer_ids=solvable_answer_ids,
            submit_slot_ids=submit_slot_ids,
        )


def _layout_slot_ids(layout: dict[str, Any]) -> set[str]:
    slots = layout.get("slots")
    if not isinstance(slots, list):
        return set()
    return {
        slot.get("id")
        for slot in slots
        if isinstance(slot, dict) and isinstance(slot.get("id"), str)
    }


def _submitted_answer_slot_ids(layout: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    slots = layout.get("slots")
    if not isinstance(slots, list):
        return out
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        content = slot.get("content")
        interaction = content.get("interaction") if isinstance(content, dict) else None
        if (
            isinstance(slot_id, str)
            and isinstance(interaction, dict)
            and interaction.get("role") == "answer"
            and interaction.get("type") == "input"
            and interaction.get("include_in_submission") is not False
        ):
            out.add(slot_id)
    return out


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
            if key == "blanks":
                slot_id = item.get("slot_id") or item.get("blank_id") or item.get("id")
            else:
                slot_id = item.get("slot_id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id.strip():
                out.add(slot_id)
    return out


def _answer_values(answer: dict[str, Any]) -> list[Any]:
    raw_value = answer.get("value")
    if isinstance(raw_value, list):
        return list(raw_value)

    answer_key = answer.get("answer_key")
    if isinstance(answer_key, list):
        values: list[Any] = []
        for item in answer_key:
            if isinstance(item, dict) and "value" in item:
                values.append(item["value"])
        if values:
            return values

    blanks = answer.get("blanks")
    if isinstance(blanks, list):
        values = []
        for item in blanks:
            if not isinstance(item, dict):
                continue
            if "expected" in item:
                values.append(item["expected"])
            elif "value" in item:
                values.append(item["value"])
        if values:
            return values

    if isinstance(raw_value, str | int | float) and not isinstance(raw_value, bool):
        return [raw_value]
    return []


def _answer_values_for_submit_slots(
    answer: dict[str, Any],
    submit_slots: list[dict[str, Any]],
) -> list[Any]:
    values = _answer_values(answer)
    if len(values) == len(submit_slots):
        return values

    indexed_values: list[Any] = []
    for submit_slot in submit_slots:
        index = _answer_key_index(submit_slot)
        if index is None or index < 0 or index >= len(values):
            return values
        indexed_values.append(values[index])
    return indexed_values


def _answer_key_index(submit_slot: dict[str, Any]) -> int | None:
    raw_index = submit_slot.get("answer_key_index")
    if isinstance(raw_index, int) and not isinstance(raw_index, bool):
        return raw_index
    if isinstance(raw_index, str):
        try:
            return int(raw_index.strip())
        except ValueError:
            pass

    answer_ref = submit_slot.get("answer_ref")
    if isinstance(answer_ref, str):
        import re

        match = re.fullmatch(r"answer_key\[(\d+)\]", answer_ref.strip())
        if match:
            return int(match.group(1))

    order = submit_slot.get("order")
    if isinstance(order, int) and not isinstance(order, bool):
        return order
    if isinstance(order, str):
        try:
            return int(order.strip())
        except ValueError:
            return None
    return None


def _assert_answer_ids_exist(
    *,
    label: str,
    answer_ids: set[str],
    layout_slot_ids: set[str],
    deleted_slots: set[str],
) -> None:
    missing = sorted(answer_ids - layout_slot_ids)
    if missing:
        deleted = sorted(
            slot_id
            for slot_id in missing
            if _deleted_slot_matches(slot_id, deleted_slots)
        )
        if deleted:
            raise AnswerContractError(
                f"{label} references deleted layout slot(s): {', '.join(deleted)}"
            )
        raise AnswerContractError(
            f"{label} references missing layout slot(s): {', '.join(missing)}"
        )


def _assert_answer_ids_match_submit_slots(
    *,
    label: str,
    answer_ids: set[str],
    submit_slot_ids: set[str],
) -> None:
    if not submit_slot_ids:
        return
    extra = sorted(answer_ids - submit_slot_ids)
    missing = sorted(submit_slot_ids - answer_ids)
    if extra or missing:
        parts: list[str] = []
        if extra:
            parts.append(f"non-submitted answer slot(s): {', '.join(extra)}")
        if missing:
            parts.append(f"missing submitted answer slot(s): {', '.join(missing)}")
        raise AnswerContractError(
            f"{label} does not match submitted answer slots: {'; '.join(parts)}"
        )


def _deleted_slot_matches(slot_id: str, deleted_slots: set[str]) -> bool:
    if slot_id in deleted_slots:
        return True
    return any(slot_id.startswith(f"{deleted}.") for deleted in deleted_slots)
