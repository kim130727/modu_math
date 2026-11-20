"""Answer-free presentation and field bindings shared with student renderers."""


def presentation_contract(problem, schema):
    answer = problem.answer
    presentation = answer.get("presentation") or {}
    review = presentation.get("review") or {}
    mode = review.get("mode") or presentation.get("mode")
    fields = schema["fields"]
    keys = answer.get("answer_key") or []
    keys = keys if isinstance(keys, list) else []
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
            slot = (element.get("refs") or {}).get("layout_slot_id")
            index = next(
                (
                    i
                    for i, key in enumerate(keys)
                    if isinstance(key, dict)
                    and any(
                        ref and ref in {key.get("slot_id"), key.get("id")}
                        for ref in (
                            reference,
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
