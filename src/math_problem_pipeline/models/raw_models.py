"""Shared and raw extraction models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BBox(BaseModel):
    """Bounding box in source PDF coordinates."""

    x0: float
    y0: float
    x1: float
    y1: float


class SourceDocument(BaseModel):
    """Top-level source document metadata."""

    document_id: str
    source_pdf: str
    page_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class RawTextBlock(BaseModel):
    """Text block extracted from a page."""

    block_id: str
    text: str
    bbox: BBox
    font_name: str | None = None
    font_size: float | None = None


class RawVisualBlock(BaseModel):
    """Visual primitive from source page (line/rect/curve/image)."""

    block_id: str
    kind: str
    bbox: BBox
    payload: dict[str, Any] = Field(default_factory=dict)


class SourcePage(BaseModel):
    """Raw extraction result for one PDF page."""

    page_id: str
    document_id: str
    source_pdf: str
    page_number: int
    width: float
    height: float
    text_blocks: list[RawTextBlock] = Field(default_factory=list)
    visual_blocks: list[RawVisualBlock] = Field(default_factory=list)


class RawProblemRegion(BaseModel):
    """Candidate problem region grouped from source blocks."""

    region_id: str
    document_id: str
    source_pdf: str
    page_number: int
    problem_number: str | None = None
    bbox: BBox
    text_block_ids: list[str] = Field(default_factory=list)
    visual_block_ids: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
