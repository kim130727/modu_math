"""Conservative problem segmentation from raw page data."""

from __future__ import annotations

import re
from dataclasses import dataclass

from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.raw_models import BBox, RawProblemRegion, SourcePage

EXPLICIT_PROBLEM_MARKER = re.compile(r"^(\d{1,2}[\.|\)]|[①②③④⑤]|[가나다라마바사][\.|\)])$")
CHOICE_MARKER = re.compile(r"[①②③④⑤]|\(?[1-5]\)")
HEADER_FOOTER_HINT = re.compile(r"학교|단원|평가|학년|학기|정답|해설|copyright|www|http|날짜|이름|점수|단위", re.IGNORECASE)
PAGE_NUMBER_ONLY = re.compile(r"^\d{1,3}$")
QUESTION_CUE_START = re.compile(r"^(다음|안에|지우개|예은이|여러|큰\s*수를|1부터)")
QUESTION_CUE_BODY = re.compile(r"구하시오|입니까|계산하시오|몇\s*개|몇\s*cm|몇\s*mm")


@dataclass
class _Line:
    text: str
    block_ids: list[str]
    x0: float
    y0: float
    x1: float
    y1: float


def segment_page_to_regions(page: SourcePage) -> list[RawProblemRegion]:
    """Split one page into problem-like regions with confidence metadata."""
    lines = _group_blocks_to_lines(page)
    content_lines = [ln for ln in lines if not _is_header_footer_line(ln, page)]
    if not content_lines:
        return []

    starts = _detect_start_points(content_lines)
    regions = _build_regions_from_starts(page, content_lines, starts)

    expanded: list[RawProblemRegion] = []
    for region in regions:
        if _is_oversized(region, page):
            split = _split_oversized_region(page, region, content_lines)
            if split:
                expanded.extend(split)
            else:
                region.notes.append("oversized_candidate")
                expanded.append(region)
        else:
            expanded.append(region)
    return expanded


def regions_to_candidates(regions: list[RawProblemRegion], page: SourcePage) -> list[ProblemCandidate]:
    text_by_id = {b.block_id: b.text for b in page.text_blocks}
    candidates: list[ProblemCandidate] = []

    for idx, region in enumerate(regions, start=1):
        text = " ".join(text_by_id.get(bid, "") for bid in region.text_block_ids).strip()
        warnings = list(region.notes)
        if not region.problem_number:
            warnings.append("missing_problem_number")
        if not CHOICE_MARKER.search(text):
            warnings.append("choice_marker_not_found")

        candidates.append(
            ProblemCandidate(
                candidate_id=f"{page.page_id}_q{idx:04d}",
                source_path=page.source_path,
                page_number=page.page_number,
                problem_number=region.problem_number,
                bbox=region.bbox,
                text=text,
                source_block_ids=list(region.text_block_ids),
                confidence=max(0.0, min(1.0, region.segmentation_score)),
                warnings=warnings,
                is_probable_problem=region.is_probable_problem,
                segmentation_reason=region.segmentation_reason,
                page_width=page.width,
                page_height=page.height,
            )
        )
    return candidates


def filter_obvious_non_problems(
    candidates: list[ProblemCandidate],
) -> tuple[list[ProblemCandidate], list[ProblemCandidate]]:
    accepted: list[ProblemCandidate] = []
    rejected: list[ProblemCandidate] = []
    for cand in candidates:
        text = cand.text.strip()
        upper_meta_without_number = (
            cand.problem_number is None
            and cand.page_height is not None
            and cand.bbox.y0 < cand.page_height * 0.28
        )
        colon_meta_line = text.count(":") >= 2 and len(text) <= 80
        bad = (
            not cand.is_probable_problem
            or len(text) < 4
            or HEADER_FOOTER_HINT.search(text)
            or PAGE_NUMBER_ONLY.match(text)
            or upper_meta_without_number
            or colon_meta_line
        )
        if bad:
            c = cand.model_copy(deep=True)
            c.warnings.append("rejected_non_problem_candidate")
            if upper_meta_without_number:
                c.warnings.append("top_meta_without_problem_number")
            if colon_meta_line:
                c.warnings.append("header_metadata_pattern_detected")
            c.is_probable_problem = False
            rejected.append(c)
        else:
            accepted.append(cand)
    return accepted, rejected


def _group_blocks_to_lines(page: SourcePage, y_tol: float = 4.0) -> list[_Line]:
    blocks = sorted(page.text_blocks, key=lambda b: (b.bbox.y0, b.bbox.x0))
    lines: list[_Line] = []
    current: list = []
    current_y: float | None = None

    for block in blocks:
        if current_y is None or abs(block.bbox.y0 - current_y) <= y_tol:
            current.append(block)
            current_y = block.bbox.y0 if current_y is None else (current_y + block.bbox.y0) / 2
            continue

        lines.append(_finalize_line(current))
        current = [block]
        current_y = block.bbox.y0

    if current:
        lines.append(_finalize_line(current))
    return lines


def _finalize_line(blocks: list) -> _Line:
    ordered = sorted(blocks, key=lambda b: b.bbox.x0)
    text = " ".join((b.text or "").strip() for b in ordered if (b.text or "").strip())
    return _Line(
        text=text,
        block_ids=[b.block_id for b in ordered],
        x0=min(b.bbox.x0 for b in ordered),
        y0=min(b.bbox.y0 for b in ordered),
        x1=max(b.bbox.x1 for b in ordered),
        y1=max(b.bbox.y1 for b in ordered),
    )


def _is_header_footer_line(line: _Line, page: SourcePage) -> bool:
    text = line.text.strip()
    if not text:
        return True

    top_ratio = line.y0 / max(page.height, 1.0)
    bottom_ratio = line.y1 / max(page.height, 1.0)

    if top_ratio < 0.12 and HEADER_FOOTER_HINT.search(text):
        return True
    if bottom_ratio > 0.93 and (PAGE_NUMBER_ONLY.match(text) or HEADER_FOOTER_HINT.search(text)):
        return True
    return False


def _detect_start_points(lines: list[_Line]) -> list[tuple[int, float, str, bool, str | None]]:
    starts: list[tuple[int, float, str, bool, str | None]] = []
    prev: _Line | None = None

    for idx, line in enumerate(lines):
        text = line.text.strip()
        if not text:
            continue

        problem_number = _extract_problem_number(text)
        if EXPLICIT_PROBLEM_MARKER.match(text.split()[0]) or problem_number is not None:
            starts.append((idx, 0.95, "explicit_problem_marker", True, problem_number))
            prev = line
            continue

        if CHOICE_MARKER.search(text) and prev is not None and (line.y0 - prev.y1) > 10:
            starts.append((idx, 0.72, "choice_pattern_after_vertical_gap", True, None))
            prev = line
            continue

        if prev is not None:
            vertical_gap = line.y0 - prev.y1
            left_shift = abs(line.x0 - prev.x0)
            if vertical_gap > 18 and left_shift < 25:
                starts.append((idx, 0.60, "layout_gap_and_alignment_change", True, None))

        prev = line

    if not starts:
        cue_starts = _detect_question_cue_starts(lines)
        if cue_starts:
            starts.extend(cue_starts)
        else:
            starts.append((0, 0.35, "fallback_single_region", False, None))
    return _dedupe_starts(starts)


def _build_regions_from_starts(
    page: SourcePage,
    lines: list[_Line],
    starts: list[tuple[int, float, str, bool, str | None]],
) -> list[RawProblemRegion]:
    out: list[RawProblemRegion] = []
    for i, (start_idx, score, reason, probable, pnum) in enumerate(starts, start=1):
        end_idx = starts[i][0] if i < len(starts) else len(lines)
        seg_lines = lines[start_idx:end_idx]
        if not seg_lines:
            continue

        bbox = BBox(
            x0=min(ln.x0 for ln in seg_lines),
            y0=min(ln.y0 for ln in seg_lines),
            x1=max(ln.x1 for ln in seg_lines),
            y1=max(ln.y1 for ln in seg_lines),
        )
        out.append(
            RawProblemRegion(
                region_id=f"{page.page_id}_r{i:04d}",
                document_id=page.document_id,
                source_path=page.source_path,
                page_number=page.page_number,
                problem_number=pnum,
                bbox=bbox,
                text_block_ids=[bid for ln in seg_lines for bid in ln.block_ids],
                visual_block_ids=[],
                notes=[],
                segmentation_score=score,
                segmentation_reason=reason,
                is_probable_problem=probable,
            )
        )
    return out


def _split_oversized_region(page: SourcePage, region: RawProblemRegion, lines: list[_Line]) -> list[RawProblemRegion]:
    in_region = [ln for ln in lines if ln.y0 >= region.bbox.y0 and ln.y1 <= region.bbox.y1]
    if len(in_region) < 2:
        return []

    secondary_starts: list[int] = [0]
    for idx in range(1, len(in_region)):
        prev = in_region[idx - 1]
        cur = in_region[idx]
        if CHOICE_MARKER.search(cur.text) and (cur.y0 - prev.y1) > 8:
            secondary_starts.append(idx)
            continue
        if (cur.y0 - prev.y1) > 24:
            secondary_starts.append(idx)

    secondary_starts = sorted(set(secondary_starts))
    if len(secondary_starts) <= 1:
        return []

    splits: list[RawProblemRegion] = []
    for i, s in enumerate(secondary_starts, start=1):
        e = secondary_starts[i] if i < len(secondary_starts) else len(in_region)
        seg_lines = in_region[s:e]
        if not seg_lines:
            continue
        bbox = BBox(
            x0=min(ln.x0 for ln in seg_lines),
            y0=min(ln.y0 for ln in seg_lines),
            x1=max(ln.x1 for ln in seg_lines),
            y1=max(ln.y1 for ln in seg_lines),
        )
        splits.append(
            RawProblemRegion(
                region_id=f"{region.region_id}_s{i:02d}",
                document_id=page.document_id,
                source_path=page.source_path,
                page_number=page.page_number,
                problem_number=region.problem_number,
                bbox=bbox,
                text_block_ids=[bid for ln in seg_lines for bid in ln.block_ids],
                visual_block_ids=[],
                notes=["oversized_candidate_split_retry"],
                segmentation_score=min(0.85, region.segmentation_score + 0.05),
                segmentation_reason=f"{region.segmentation_reason}+oversized_split_retry",
                is_probable_problem=True,
            )
        )
    return splits


def _is_oversized(region: RawProblemRegion, page: SourcePage) -> bool:
    h = max(0.0, region.bbox.y1 - region.bbox.y0)
    return h >= page.height * 0.5


def _extract_problem_number(text: str) -> str | None:
    m = re.match(r"^(\d{1,2})[\.|\)]", text)
    if m:
        return m.group(1)
    return None


def _dedupe_starts(starts: list[tuple[int, float, str, bool, str | None]]) -> list[tuple[int, float, str, bool, str | None]]:
    best_by_idx: dict[int, tuple[int, float, str, bool, str | None]] = {}
    for item in starts:
        idx, score, _, _, _ = item
        old = best_by_idx.get(idx)
        if old is None or score > old[1]:
            best_by_idx[idx] = item
    return [best_by_idx[k] for k in sorted(best_by_idx)]









def _detect_question_cue_starts(lines: list[_Line]) -> list[tuple[int, float, str, bool, str | None]]:
    starts: list[tuple[int, float, str, bool, str | None]] = []
    for idx, line in enumerate(lines):
        text = line.text.strip()
        if not text:
            continue
        if QUESTION_CUE_START.search(text):
            starts.append((idx, 0.62, "question_cue_start", True, None))
            continue
        if QUESTION_CUE_BODY.search(text) and len(text) >= 10:
            starts.append((idx, 0.55, "question_cue_body", True, None))

    if starts and starts[0][0] != 0:
        starts.insert(0, (0, 0.50, "question_cue_implicit_first", True, None))
    return _dedupe_starts(starts)

