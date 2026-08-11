from __future__ import annotations

from typing import Any


class AnswerContractError(ValueError):
    pass


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
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id.strip():
                out.add(slot_id)
    return out


def _assert_answer_ids_exist(
    *,
    label: str,
    answer_ids: set[str],
    layout_slot_ids: set[str],
    deleted_slots: set[str],
) -> None:
    missing = sorted(answer_ids - layout_slot_ids)
    if missing:
        deleted = sorted(slot_id for slot_id in missing if _deleted_slot_matches(slot_id, deleted_slots))
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
        raise AnswerContractError(f"{label} does not match submitted answer slots: {'; '.join(parts)}")


def _deleted_slot_matches(slot_id: str, deleted_slots: set[str]) -> bool:
    if slot_id in deleted_slots:
        return True
    return any(slot_id.startswith(f"{deleted}.") for deleted in deleted_slots)
