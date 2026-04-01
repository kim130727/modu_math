"""Heuristic problem segmentation from raw page data."""

from __future__ import annotations

import re

from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.raw_models import BBox, RawProblemRegion, SourcePage

PROBLEM_MARKER = re.compile(r"^(\d+)[\.|\)]$")
CHOICE_MARKER = re.compile(r"^[①②③④⑤]|^\(?[1-5]\)")


def segment_page_to_regions(page: SourcePage) -> list[RawProblemRegion]:
    """Split a page into problem regions based on number markers.

    TODO: replace this with robust OCR-aware line grouping.
    """
    sorted_blocks = sorted(page.text_blocks, key=lambda b: (b.bbox.y0, b.bbox.x0))
    regions: list[RawProblemRegion] = []

    current_blocks = []
    current_problem_number: str | None = None
    region_idx = 1

    for block in sorted_blocks:
        token = block.text.strip()
        if PROBLEM_MARKER.match(token):
            if current_blocks:
                regions.append(
                    _build_region(
                        page=page,
                        region_idx=region_idx,
                        problem_number=current_problem_number,
                        blocks=current_blocks,
                    )
                )
                region_idx += 1
            current_problem_number = token.rstrip(".)")
            current_blocks = [block]
        else:
            current_blocks.append(block)

    if current_blocks:
        regions.append(
            _build_region(
                page=page,
                region_idx=region_idx,
                problem_number=current_problem_number,
                blocks=current_blocks,
            )
        )

    return regions


def regions_to_candidates(regions: list[RawProblemRegion], page: SourcePage) -> list[ProblemCandidate]:
    text_by_id = {b.block_id: b.text for b in page.text_blocks}
    candidates: list[ProblemCandidate] = []
    for idx, region in enumerate(regions, start=1):
        text = " ".join(text_by_id.get(bid, "") for bid in region.text_block_ids).strip()
        warnings = []
        if not region.problem_number:
            warnings.append("missing_problem_number")
        if not CHOICE_MARKER.search(text):
            warnings.append("choice_marker_not_found")

        candidates.append(
            ProblemCandidate(
                candidate_id=f"{page.page_id}_q{idx:04d}",
                document_id=page.document_id,
                source_pdf=page.source_pdf,
                page_number=page.page_number,
                problem_number=region.problem_number,
                bbox=region.bbox,
                text=text,
                raw_region_id=region.region_id,
                confidence=0.55,
                warnings=warnings,
            )
        )
    return candidates


def _build_region(
    page: SourcePage,
    region_idx: int,
    problem_number: str | None,
    blocks,
) -> RawProblemRegion:
    x0 = min(b.bbox.x0 for b in blocks)
    y0 = min(b.bbox.y0 for b in blocks)
    x1 = max(b.bbox.x1 for b in blocks)
    y1 = max(b.bbox.y1 for b in blocks)
    return RawProblemRegion(
        region_id=f"{page.page_id}_r{region_idx:04d}",
        document_id=page.document_id,
        source_pdf=page.source_pdf,
        page_number=page.page_number,
        problem_number=problem_number,
        bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1),
        text_block_ids=[b.block_id for b in blocks],
        visual_block_ids=[],
        notes=[],
    )
