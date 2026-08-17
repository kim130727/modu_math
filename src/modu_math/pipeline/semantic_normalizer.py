from __future__ import annotations

from typing import Any


def normalize_semantic_for_schema(
    semantic: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """Normalize permissive generated semantic fields into schema-safe shapes."""
    changed = False
    normalized = dict(semantic)
    understanding = normalized.get("understanding")
    if not isinstance(understanding, dict):
        return semantic, False

    questions = understanding.get("diagnostic_questions")
    if not isinstance(questions, list):
        return semantic, False

    normalized_questions: list[Any] = []
    for question in questions:
        if not isinstance(question, dict):
            normalized_questions.append(question)
            continue
        choices = question.get("choices")
        if not isinstance(choices, list) or all(
            isinstance(choice, str) for choice in choices
        ):
            normalized_questions.append(question)
            continue
        normalized_question = dict(question)
        normalized_question["choices"] = [str(choice) for choice in choices]
        normalized_questions.append(normalized_question)
        changed = True

    if not changed:
        return semantic, False

    normalized_understanding = dict(understanding)
    normalized_understanding["diagnostic_questions"] = normalized_questions
    normalized["understanding"] = normalized_understanding
    return normalized, True
