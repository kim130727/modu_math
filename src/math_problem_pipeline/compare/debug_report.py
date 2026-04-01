"""Schema refinement oriented debug report generation."""

from __future__ import annotations

from pathlib import Path

from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.semantic_models import SemanticProblem
from math_problem_pipeline.normalize.validators import validate_candidate
from math_problem_pipeline.utils.io import write_json


def build_schema_refinement_report(
    candidate: ProblemCandidate,
    semantic: SemanticProblem,
    render_meta: dict,
) -> dict:
    anomaly_flags = sorted(set(candidate.warnings + validate_candidate(candidate) + semantic.warnings))
    fallback_used = bool(render_meta.get("fallback_render_used"))
    rejected = bool(getattr(semantic, "rejected", False) or semantic.type == "rejected_candidate")

    recommended_action = _recommended_action(rejected, fallback_used, anomaly_flags)

    report = {
        "problem_id": semantic.problem_id,
        "source_path": semantic.source_path,
        "page_number": semantic.page_number,
        "type_guess": semantic.type_guess,
        "type_guess_reason": semantic.type_guess_reason,
        "rejected": rejected,
        "fallback_render_used": fallback_used,
        "anomaly_flags": anomaly_flags,
        "recommended_action": recommended_action,
        "raw_fields": {
            "text": candidate.text,
            "bbox": candidate.bbox.model_dump(),
            "warnings": candidate.warnings,
            "is_probable_problem": candidate.is_probable_problem,
            "segmentation_reason": candidate.segmentation_reason,
            "source_block_ids": candidate.source_block_ids,
        },
        "semantic_fields": semantic.model_dump(),
        "renderer_usage": render_meta,
    }
    return report


def write_report(report: dict, output_path: Path) -> None:
    write_json(output_path, report)


def _recommended_action(rejected: bool, fallback_used: bool, anomaly_flags: list[str]) -> str:
    if rejected:
        return "resegment_required"
    if "merged_multiple_problems_suspected" in anomaly_flags or "oversized_candidate" in anomaly_flags:
        return "resegment_required"
    if fallback_used or "visual_structure_detection_needed" in anomaly_flags:
        return "structure_detection_needed"
    if anomaly_flags:
        return "manual_review_required"
    return "safe_to_render"

