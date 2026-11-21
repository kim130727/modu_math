"""Answer-free presentation and field bindings shared with student renderers."""

from collections import Counter
import re


def normalize_answer_capacity(elements, presentation):
    """A whole-answer box must not inherit a digit-cell's length restriction.

    Use a uniform public limit, independent of the secret answer's length.
    Preserve explicit digit cells, and capacities of cells composing one field.
    """
    bindings = presentation.get("canvas_bindings", {})
    counts = Counter(bindings.values())
    for element in elements:
        field = bindings.get(str(element.get("id")))
        interaction = element.get("interaction") or {}
        if (
            field is None or counts[field] != 1
            or interaction.get("role") != "answer"
            or interaction.get("value_type") in {"digit", "digits", "operator", "comparison_operator"}
            or interaction.get("keyboard") == "operator"
        ):
            continue
        interaction["max_length"] = 64
        interaction["auto_advance"] = False
        element["interaction"] = interaction


def presentation_contract(problem, schema):
    answer = problem.answer
    presentation = answer.get("presentation") or {}
    review = presentation.get("review") or {}
    mode = review.get("mode") or presentation.get("mode")
    fields = schema["fields"]
    keys = answer.get("answer_key") or []
    keys = keys if isinstance(keys, list) else []
    candidates = [e for e in problem.renderer_data.get("elements", [])
                  if (e.get("interaction") or {}).get("role") == "answer"
                  and (e.get("interaction") or {}).get("include_in_submission") is not False]
    orders = [(e.get("interaction") or {}).get("order") for e in candidates]
    # A complete authored field order is an explicit legacy binding. Copied
    # visual slots may still have stale answer-key IDs; renderer array order
    # and tiny coordinate differences must never determine grading order.
    ordered_fields = (len(orders) == len(fields)
                      and all(isinstance(o, int) and not isinstance(o, bool) for o in orders)
                      and set(orders) == set(range(len(fields))))
    bindings = {}
    for element in problem.renderer_data.get("elements", []):
        interaction = element.get("interaction") or {}
        if (
            element.get("type") not in {"rect", "circle", "text_box"}
            or interaction.get("role") != "answer"
            or interaction.get("include_in_submission") is False
        ):
            continue
        geometry = element.get("attributes") or {}
        dimensions = (
            [geometry.get("r")]
            if element["type"] == "circle"
            else [geometry.get("width"), geometry.get("height")]
        )
        if not all(
            isinstance(value, (int, float)) and value > 0 for value in dimensions
        ):
            continue
        index = interaction.get("answer_key_index")
        if not isinstance(index, int) or isinstance(index, bool):
            reference = interaction.get("answer_ref")
            index = next((i for i, key in enumerate(keys)
                          if isinstance(key, dict) and reference
                          and reference in {key.get("slot_id"), key.get("id")}), None)
            if index is None and isinstance(reference, str):
                pointer = re.fullmatch(r"answer_key\[(\d+)\]", reference)
                if pointer:
                    index = int(pointer.group(1))
            if index is None and ordered_fields:
                index = interaction["order"]
        if index is None:
            slot = (element.get("refs") or {}).get("layout_slot_id")
            index = next(
                (
                    i
                    for i, key in enumerate(keys)
                    if isinstance(key, dict)
                    and any(
                        ref and ref in {key.get("slot_id"), key.get("id")}
                        for ref in (
                            slot,
                            element.get("source_ref"),
                            element.get("id"),
                        )
                    )
                ),
                None,
            )
        if index is None:
            index = 0 if len(fields) == 1 else interaction.get("order")
        if (
            isinstance(index, int)
            and not isinstance(index, bool)
            and 0 <= index < len(fields)
        ):
            bindings[str(element["id"])] = index
    if not mode:
        mode = "canvas_slots" if bindings else "panel_input"
    # Keep every answer reachable when an older document has partial bindings.
    if mode == "canvas_slots" and (
        review.get("show_canvas") is False
        or set(bindings.values()) != set(range(len(fields)))
        or any(field["type"] not in {"number", "text"} for field in fields)
    ):
        mode = "panel_input"
    return {
        "mode": mode,
        "show_canvas": review.get("show_canvas", True),
        "canvas_bindings": bindings if mode == "canvas_slots" else {},
    }


def safe_layout(layout):
    return {
        "regions": [
            {"role": r.get("role"), "slot_ids": r.get("slot_ids", [])}
            for r in layout.get("regions", [])
        ],
        "slots": [
            {
                "id": s.get("id"),
                "content": {
                    key: s["content"][key]
                    for key in ("semantic_role", "style_role")
                    if key in (s.get("content") or {})
                },
            }
            for s in layout.get("slots", [])
        ],
    }


def authored_prompt(problem):
    layout = problem.layout_data
    top_ids = {
        str(slot)
        for region in layout.get("regions", [])
        if region.get("role") in {"question", "instruction"}
        for slot in region.get("slot_ids", [])
    }
    texts = []
    for slot in layout.get("slots", []):
        content = slot.get("content") or {}
        role = content.get("semantic_role") or content.get("style_role")
        if role in {"question", "instruction"} or (
            not role and str(slot.get("id")) in top_ids
        ):
            text = content.get("text")
            if isinstance(text, str) and text.strip() and text not in texts:
                texts.append(text)
    return "\n".join(texts)
