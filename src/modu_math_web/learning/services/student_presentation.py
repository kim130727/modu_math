"""Answer-free presentation and field bindings shared with student renderers."""

from collections import Counter
import re

from .assignment_content import answer_field_values


def normalize_answer_capacity(elements, presentation, answer, schema):
    """A whole-answer box must not inherit a digit-cell's length restriction.

    Use the field's integer limit for whole answers and preserve split cells.
    """
    bindings = presentation.get("canvas_bindings", {})
    counts = Counter(bindings.values())
    values = answer_field_values(answer)
    fields = schema["fields"]
    for element in elements:
        field = bindings.get(str(element.get("id")))
        interaction = element.get("interaction") or {}
        if (
            type(field) is not int or not 0 <= field < len(fields) or counts[field] != 1
            or interaction.get("role") != "answer"
            or interaction.get("value_type") in {"operator", "comparison_operator"}
            or interaction.get("keyboard") == "operator"
        ):
            continue
        limit = fields[field].get("max_length")
        if limit is not None:
            if limit == 1 and interaction.get("value_type") in {"digit", "digits"}:
                element["interaction"] = {**interaction, "max_length": 1}
            else:
                element["interaction"] = {
                    **interaction, "value_type": "integer", "keyboard": "number",
                    "max_length": limit, "auto_advance": False,
                }
            continue
        interaction = {**interaction, "max_length": 64, "auto_advance": False}
        if interaction.get("value_type") in {"digit", "digits"}:
            expected = values[field] if field < len(values) else None
            if expected is None:
                continue
            kind = fields[field]["type"]
            interaction["value_type"] = "number" if kind == "number" else "text"
            interaction["keyboard"] = "decimal" if kind == "number" else "text"
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
    canvas_choices = []
    if mode == "canvas_select":
        elements = problem.renderer_data.get("elements", [])
        raw_choices = answer.get("choices") or []
        for index, choice in enumerate(raw_choices if isinstance(raw_choices, list) else []):
            if not isinstance(choice, dict):
                continue
            choice_id = str(choice.get("id") or f"choice.{index + 1}")
            refs = set()
            for ref in choice.get("source_refs") or []:
                if isinstance(ref, str) and ref.strip():
                    refs.add(ref.strip())
            if isinstance(choice.get("slot_id"), str) and choice["slot_id"].strip():
                refs.add(choice["slot_id"].strip())
            refs.add(choice_id)
            matched_ids = []
            for element in elements:
                if not isinstance(element, dict):
                    continue
                el_id = str(element.get("id") or "")
                source_ref = str(element.get("source_ref") or "")
                layout_slot_id = str((element.get("refs") or {}).get("layout_slot_id") or "")
                if any(candidate and candidate in refs for candidate in (el_id, source_ref, layout_slot_id)):
                    if el_id:
                        matched_ids.append(el_id)
            if matched_ids:
                canvas_choices.append({
                    "choice_id": choice_id,
                    "value": choice_id if review.get("mode") == "canvas_select" else str(choice.get("text") or choice.get("label") or choice_id),
                    "label": str(choice.get("text") or choice.get("label") or f"{index + 1}"),
                    "element_ids": matched_ids,
                })
        if not canvas_choices or len(canvas_choices) != len(raw_choices) or review.get("show_canvas") is False:
            mode = "choice"
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
        **(
            {
                "canvas_choices": canvas_choices,
                "multi": len(keys) > 1
                or (not review and answer.get("target", {}).get("type") == "multiple_choice_set"),
            }
            if mode == "canvas_select"
            else {}
        ),
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


def student_prompt(problem):
    metadata = problem.semantic_data.get("metadata") or {}
    return (
        authored_prompt(problem)
        or metadata.get("presentation_prompt")
        or metadata.get("question")
        or metadata.get("instruction")
        or ""
    )
