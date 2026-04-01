"""Simple layout engine for static problem scenes."""

from __future__ import annotations

from math_problem_pipeline.models.render_models import LayoutHint


DEFAULT_SCENE_WIDTH = 14.0
DEFAULT_SCENE_HEIGHT = 8.0


def resolve_question_position(layout_hint: LayoutHint) -> tuple[float, float]:
    if layout_hint.question_anchor:
        return layout_hint.question_anchor
    return (-6.2, 3.2)


def resolve_choices_position(layout_hint: LayoutHint) -> tuple[float, float]:
    if layout_hint.choices_anchor:
        return layout_hint.choices_anchor
    return (-6.0, 1.8)
