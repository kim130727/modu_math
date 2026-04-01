"""Render-level models for reusable scene generation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LayoutHint(BaseModel):
    """Render layout preferences in render coordinates."""

    question_anchor: tuple[float, float] | None = None
    choices_anchor: tuple[float, float] | None = None
    relative_position: str | None = None
    alignment: str = "left"


class StyleHint(BaseModel):
    """Visual style preferences for renderer."""

    font_size: int = 30
    stroke_width: float = 2.0
    primary_color: str = "#1f2937"
    accent_color: str = "#2563eb"


class FigureSpec(BaseModel):
    """Generic figure payload consumed by type builders."""

    figure_type: str
    semantic_coordinates: dict = Field(default_factory=dict)
    source_bbox: dict | None = None


class RenderSpec(BaseModel):
    """Input contract to renderer after semantic normalization."""

    problem_id: str
    semantic_type: str
    question_text: str
    layout_hint: LayoutHint = Field(default_factory=LayoutHint)
    style_hint: StyleHint = Field(default_factory=StyleHint)
    figures: list[FigureSpec] = Field(default_factory=list)
    choices: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
