"""Schema refinement oriented debug report generation."""

from __future__ import annotations

from pathlib import Path

from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.semantic_models import (
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    SemanticProblem,
)
from math_problem_pipeline.utils.io import write_json


def build_schema_refinement_report(
    candidate: ProblemCandidate,
    semantic: SemanticProblem,
    render_meta: dict,
) -> dict:
    missing = []
    simplifications = []
    improvement_points = []

    if semantic.type == "multiple_choice_text" and not getattr(semantic, "choices", []):
        missing.append("choices")
        improvement_points.append("choice_positions_not_available")

    if isinstance(semantic, FractionShadedAreaProblem):
        if semantic.fraction.partition == "grid" and (semantic.fraction.rows is None or semantic.fraction.cols is None):
            missing.append("fraction.rows_or_cols")
            improvement_points.append("ambiguous_fraction_partition")

    if isinstance(semantic, GeometryBasicProblem) and not semantic.points:
        missing.append("geometry.points")
        improvement_points.append("missing_geometry_vertices")

    if semantic.type == "clock_reading":
        clock = getattr(semantic, "clock", None)
        if clock and clock.hour_angle is None and clock.minute_angle is None:
            simplifications.append("clock_hand_angle_inferred")

    if semantic.render_hint.question_anchor is None:
        simplifications.append("fallback_layout_used")

    report = {
        "problem_id": semantic.problem_id,
        "source_pdf": semantic.source_pdf,
        "page_number": semantic.page_number,
        "raw_fields": {
            "text": candidate.text,
            "bbox": candidate.bbox.model_dump(),
            "warnings": candidate.warnings,
        },
        "semantic_fields": semantic.model_dump(),
        "renderer_usage": render_meta,
        "missing_information": missing,
        "simplifications": simplifications,
        "schema_refinement_points": sorted(set(improvement_points + semantic.warnings)),
    }
    return report


def write_report(report: dict, output_path: Path) -> None:
    write_json(output_path, report)
