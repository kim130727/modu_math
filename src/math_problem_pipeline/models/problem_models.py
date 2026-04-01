"""Problem-level intermediate models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .raw_models import BBox


class ProblemCandidate(BaseModel):
    """Raw candidate with conservative segmentation metadata."""

    candidate_id: str
    source_path: str
    page_number: int
    problem_number: str | None = None
    bbox: BBox
    text: str
    source_block_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    warnings: list[str] = Field(default_factory=list)
    is_probable_problem: bool = True
    segmentation_reason: str = "unknown"
    page_width: float | None = None
    page_height: float | None = None


class ExtractedProblem(BaseModel):
    """Candidate with conservative type-guess metadata."""

    problem_id: str
    candidate_id: str
    source_path: str
    page_number: int
    problem_number: str | None = None
    type_guess: str
    type_guess_reason: str
    type_confidence: float
    question_text: str
    choices: list[str] = Field(default_factory=list)
    answer_hint: str | None = None
    bbox: BBox
    segmentation_confidence: float = 0.0
    structure_confidence: float = 0.0
    warnings: list[str] = Field(default_factory=list)
    is_probable_problem: bool = True
    page_width: float | None = None
    page_height: float | None = None

