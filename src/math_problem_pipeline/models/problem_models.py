"""Problem-level intermediate models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .raw_models import BBox


class ProblemCandidate(BaseModel):
    """Problem candidate grouped from raw page content."""

    candidate_id: str
    document_id: str
    source_pdf: str
    page_number: int
    problem_number: str | None = None
    bbox: BBox
    text: str
    raw_region_id: str
    confidence: float = 0.0
    warnings: list[str] = Field(default_factory=list)


class ExtractedProblem(BaseModel):
    """Problem candidate with preliminary structural extraction."""

    problem_id: str
    candidate_id: str
    source_pdf: str
    page_number: int
    problem_number: str | None = None
    type_guess: str
    question_text: str
    choices: list[str] = Field(default_factory=list)
    answer_hint: str | None = None
    bbox: BBox
    confidence: float = 0.0
    warnings: list[str] = Field(default_factory=list)
