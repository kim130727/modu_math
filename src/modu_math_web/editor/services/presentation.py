"""Restore authoring roles and synchronize presentation from the final layout.

Never classify text by its position alone: a diagram label is not a question.
Keep the full layout for editing; the solving client projects its visual layer.
"""
from __future__ import annotations

from copy import deepcopy
import re
from typing import Any


def structure_presentation(layout: dict, semantic: dict, solvable: dict | None = None):
    layout, semantic, solvable = deepcopy((layout, semantic, solvable))
    metadata = semantic.setdefault("metadata", {})
    region_roles = {
        slot_id: region.get("role")
        for region in layout.get("regions", [])
        for slot_id in region.get("slot_ids", [])
    }
    texts: dict[str, list[dict]] = {"question": [], "instruction": [], "choice": []}
    for slot in layout.get("slots", []):
        if slot.get("kind") not in {"text", "text_box", "label"}:
            continue
        content = slot.get("content", {})
        text = content.get("text")
        if not isinstance(text, str):
            continue
        identity = slot.get("id", "").lower()
        role = content.get("semantic_role")
        if not role or role in {"text", "unknown"}:
            if re.search(r"(?:^|[._])(?:instruction)(?:[._]|$)", identity):
                role = "instruction"
            elif (re.search(r"(?:^|[._])(?:question|stem|q\d*|q_text)(?:[._]|$)", identity)
                  or content.get("style_role") == "question"
                  or region_roles.get(slot.get("id")) == "stem"
                  or text.strip() == str(metadata.get("question", "")).strip()):
                role = "question"
            elif re.search(r"(?:^|[._])(?:choice|option|opt)[._]?\d+(?:[._]|$)", identity):
                role = "choice"
        if role in texts:
            content["semantic_role"] = role
            texts[role].append(slot)

    for role in ("question", "instruction"):
        if texts[role]:
            metadata[role] = "\n".join(
                slot["content"]["text"].strip() for slot in texts[role]
                if slot["content"]["text"].strip()
            )
        elif metadata.get("presentation_sources", {}).get(role):
            metadata[role] = ""
    metadata["presentation_sources"] = {
        role: [slot["id"] for slot in slots] for role, slots in texts.items()
    }

    # Only include presentation roles that actually exist in the layout slots.
    prompt_roles = [role for role in ("question", "instruction") if texts[role]]
    if not prompt_roles:
        if metadata.get("question"):
            prompt_roles = ["question"]
        elif metadata.get("instruction"):
            prompt_roles = ["instruction"]

    metadata["presentation_prompt"] = "\n".join(dict.fromkeys(
        metadata.get(role, "").strip() for role in prompt_roles
        if isinstance(metadata.get(role), str) and metadata[role].strip()
    ))

    # Bind complete textual options to their slots. Do not flatten grouped or
    # graphical choices, nor rewrite answer keys based on display text.
    choices = texts["choice"]
    for document in (semantic, solvable):
        if not document or not choices:
            continue
        answer = document.setdefault("answer", {})
        if answer.get("choice_groups"):
            continue
        previous = answer.get("choices", [])
        placeholders = all(isinstance(item, dict) and not item.get("text") and not item.get("value")
                           for item in previous)
        bound = bool(previous) and all(isinstance(item, dict) and item.get("slot_id") for item in previous)
        if previous and len(previous) != len(choices) and not placeholders and not bound:
            continue
        updated = []
        replacements = {}
        for index, slot in enumerate(choices):
            old: Any = next((item for item in previous if isinstance(item, dict)
                            and item.get("slot_id") == slot["id"]),
                           previous[index] if not bound and index < len(previous) else {})
            text = slot["content"]["text"].strip()
            old_text = old.get("text", old.get("value")) if isinstance(old, dict) else old
            if isinstance(old_text, str) and old_text:
                replacements[old_text] = text
                old_plain = re.sub(r"^\s*(?:\([1-9]\)|[①-⑩]|[1-9][.)])\s*", "", old_text)
                new_plain = re.sub(r"^\s*(?:\([1-9]\)|[①-⑩]|[1-9][.)])\s*", "", text)
                replacements[old_plain] = new_plain
            if isinstance(old, dict):
                entry = {**old, "text": text, "slot_id": slot["id"]}
                entry.setdefault("id", slot["id"])
            else:
                entry = {"id": slot["id"], "slot_id": slot["id"], "text": text, "value": old}
            updated.append(entry)
        answer["choices"] = updated
        # A literal answer follows its bound choice's edited text. IDs, numeric
        # indices, diagnostics, and mathematical solution steps remain intact.
        def replace_literal(value):
            if isinstance(value, str):
                return replacements.get(value, value)
            if isinstance(value, list):
                return [replace_literal(item) for item in value]
            if isinstance(value, dict):
                return {key: replace_literal(item) if key in {"value", "values"} else item
                        for key, item in value.items()}
            return value
        for key in ("value", "values", "answer_key"):
            if key in answer:
                answer[key] = replace_literal(answer[key])
    return layout, semantic, solvable


def structure_artifacts(artifacts: dict) -> dict:
    if not isinstance(artifacts.get("layout"), dict) or not isinstance(artifacts.get("semantic"), dict):
        return artifacts
    layout, semantic, solvable = structure_presentation(
        artifacts["layout"], artifacts["semantic"], artifacts.get("solvable")
    )
    renderer = deepcopy(artifacts.get("renderer"))
    roles = {s["id"]: s.get("content", {}).get("semantic_role") for s in layout.get("slots", [])}
    if isinstance(renderer, dict):
        for element in renderer.get("elements", []):
            role = roles.get(element.get("source_ref"))
            if role:
                element.setdefault("attributes", {})["data-semantic-role"] = role
    return {**artifacts, "layout": layout, "semantic": semantic, "solvable": solvable, "renderer": renderer}
