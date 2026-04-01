"""Conservative problem segmentation from raw page data."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from math_problem_pipeline.models.problem_models import ProblemCandidate, ProblemSubItem
from math_problem_pipeline.models.raw_models import BBox, RawProblemRegion, RawSubItem, SourcePage

# Thresholds
HEADER_TOP_RATIO = 0.12
FOOTER_BOTTOM_RATIO = 0.93
MAX_ATTACH_GAP = 26.0
HARD_SPLIT_GAP = 42.0
OVERSIZED_REGION_RATIO = 0.50
MERGED_REGION_RATIO = 0.42
MERGED_BLOCK_COUNT = 8

# Warnings
W_REJECTED_NON_PROBLEM = "rejected_non_problem_candidate"
W_HARD_REJECT = "hard_reject"
W_SOFT_PROBLEM = "soft_problem_candidate"
W_MERGED_SUSPECTED = "merged_problem_suspected"
W_TRUNCATED_SUSPECTED = "truncated_problem_suspected"
W_OVERSIZED = "oversized_candidate"
W_OVERSIZED_RETRY = "oversized_candidate_split_retry"
W_COMPOSITE = "composite_problem_detected"
W_PLACEHOLDER_MIXED = "placeholder_mixed_with_text"
W_TOP_META = "top_meta_without_problem_number"
W_HEADER_PATTERN = "header_metadata_pattern_detected"

EXPLICIT_PROBLEM_MARKER = re.compile(r"^(\d{1,2}[\.|\)]|[①②③④⑤⑥⑦⑧⑨⑩]|[가나다라마바사아자차카타파하][\.|\)])")
PROBLEM_NUMBER = re.compile(r"^(\d{1,2})[\.|\)]")
CHOICE_MARKER = re.compile(r"^(?:[①②③④⑤]|\(?[1-5]\)|ㄱ\.|ㄴ\.|ㄷ\.)")
SUBITEM_MARKER = re.compile(r"^(?:\((\d+)\)|([①②③④⑤⑥⑦⑧⑨⑩])|([ㄱㄴㄷㄹㅁㅂㅅㅇ]))")
QUESTION_ENDING = re.compile(r"(?:\?|\.\s*$|입니까\??|구하시오\.?|계산하시오\.?|옳은\s*것(?:은|을)|알맞은\s*수|모두\s*몇\s*개입니까|몇\s*(?:cm|mm|분|시))")
QUESTION_START = re.compile(r"^(?:다음|안에|지우개|예은이|여러|큰\s*수를|1부터|영화가|시계를|시계)" )
QUESTION_BODY = re.compile(r"(구하시오|입니까|계산하시오|옳은\s*것|알맞은\s*수|모두\s*몇\s*개|몇\s*(?:cm|mm|분|시))")

HEADER_FOOTER_HINT = re.compile(r"학교|단원|평가|학년|학기|정답|해설|copyright|www|http|페이지", re.IGNORECASE)
META_HINT = re.compile(r"날짜|이름|점수|학년|반|번호|정답|date|name|score", re.IGNORECASE)
PAGE_NUMBER_ONLY = re.compile(r"^\d{1,3}$")
COLON_META = re.compile(r".+:\s*.+")

PLACEHOLDER_FORMULA = re.compile(r"수식입니다\.?$")
PLACEHOLDER_SHAPE = re.compile(r"(?:모서리가\s*둥근)?사각형입니다\.?$|원입니다\.?$|삼각형입니다\.?$")
PLACEHOLDER_IMAGE = re.compile(r"그림입니다\.?$|원본\s*그림의\s*이름")
PLACEHOLDER_GENERIC = re.compile(r"도형입니다\.?$|표입니다\.?$|그래프입니다\.?$")


@dataclass
class _Line:
    text: str
    block_ids: list[str]
    x0: float
    y0: float
    x1: float
    y1: float
    role: str = "text"


@dataclass
class _StartDecision:
    is_start: bool
    score: float
    reason: str
    is_probable_problem: bool
    problem_number: str | None = None


@dataclass
class _GroupState:
    lines: list[_Line] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    start_reason: str = "unknown"
    start_score: float = 0.35
    is_probable_problem: bool = True
    problem_number: str | None = None

    def add_line(self, line: _Line) -> None:
        self.lines.append(line)

    @property
    def last_line(self) -> _Line | None:
        return self.lines[-1] if self.lines else None

    @property
    def line_count(self) -> int:
        return len(self.lines)


def segment_page_to_regions(page: SourcePage) -> list[RawProblemRegion]:
    """Split one page into problem-like regions with confidence metadata."""
    lines = _group_blocks_to_lines(page)
    content_lines = [ln for ln in lines if not _is_header_footer_line(ln, page)]
    if not content_lines:
        # Keep meta-only pages segmentable so reject-stage can classify them explicitly.
        content_lines = lines
    if not content_lines:
        return []

    grouped = _group_lines_into_candidates(content_lines, page)
    grouped = _split_merged_groups_second_pass(grouped, page)

    regions: list[RawProblemRegion] = []
    for idx, group in enumerate(grouped, start=1):
        region = _group_to_region(group, page, idx)
        if _is_oversized(region, page):
            region.notes.append(W_OVERSIZED)
            split_regions = _split_oversized_region(page, region, content_lines)
            if split_regions:
                regions.extend(split_regions)
                continue
        regions.append(region)
    return regions


def regions_to_candidates(regions: list[RawProblemRegion], page: SourcePage) -> list[ProblemCandidate]:
    text_by_id = {b.block_id: b.text for b in page.text_blocks}
    block_by_id = {b.block_id: b for b in page.text_blocks}
    candidates: list[ProblemCandidate] = []

    for idx, region in enumerate(regions, start=1):
        text = " ".join(text_by_id.get(bid, "") for bid in region.text_block_ids).strip()
        warnings = list(region.notes)
        if not region.problem_number:
            warnings.append("missing_problem_number")
        if not CHOICE_MARKER.search(text):
            warnings.append("choice_marker_not_found")

        subitems = [
            ProblemSubItem(
                label=s.label,
                text=s.text,
                source_block_ids=s.source_block_ids,
                bbox=s.bbox,
            )
            for s in region.subitems
        ]

        if not subitems:
            subitems = _extract_subitems_from_ids(region.text_block_ids, text_by_id, block_by_id)
            if subitems:
                warnings.append(W_COMPOSITE)

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
                warnings=sorted(set(warnings)),
                is_probable_problem=region.is_probable_problem,
                segmentation_reason=region.segmentation_reason,
                page_width=page.width,
                page_height=page.height,
                subitems=subitems,
                image_ids=list(page.page_image_ids),
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
        hard_reject = _is_hard_reject_candidate(cand)
        probable_by_text = _is_question_like_text(text)

        if hard_reject and not probable_by_text:
            c = cand.model_copy(deep=True)
            c.warnings.extend([W_REJECTED_NON_PROBLEM, W_HARD_REJECT])
            if _is_top_meta_without_number(c):
                c.warnings.append(W_TOP_META)
            if _looks_like_header_metadata_pattern(text):
                c.warnings.append(W_HEADER_PATTERN)
            c.warnings = sorted(set(c.warnings))
            c.is_probable_problem = False
            rejected.append(c)
            continue

        c = cand.model_copy(deep=True)
        if _has_truncated_signal(c):
            c.warnings.append(W_TRUNCATED_SUSPECTED)
        if _has_merged_signal(c):
            c.warnings.append(W_MERGED_SUSPECTED)
        if not probable_by_text:
            c.warnings.append(W_SOFT_PROBLEM)
        c.warnings = sorted(set(c.warnings))
        accepted.append(c)

    return accepted, rejected


def detect_problem_start(block: _Line, prev_block: _Line | None, next_block: _Line | None) -> _StartDecision:
    """Decide whether block starts a new problem region."""
    text = block.text.strip()
    if not text:
        return _StartDecision(False, 0.0, "empty", False, None)

    if block.role in {"header_meta", "score_meta"}:
        return _StartDecision(False, 0.05, "meta_line", False, None)

    problem_number = _extract_problem_number(text)
    if EXPLICIT_PROBLEM_MARKER.match(text):
        return _StartDecision(True, 0.95, "explicit_problem_marker", True, problem_number)

    if QUESTION_START.search(text) and QUESTION_BODY.search(text):
        return _StartDecision(True, 0.78, "question_cue_start", True, None)

    if QUESTION_ENDING.search(text) and (prev_block is None or (block.y0 - prev_block.y1) > 14):
        return _StartDecision(True, 0.70, "question_sentence_after_gap", True, None)

    if CHOICE_MARKER.search(text) and prev_block is not None and (block.y0 - prev_block.y1) > 16:
        return _StartDecision(True, 0.62, "choice_pattern_after_vertical_gap", True, None)

    if next_block and QUESTION_START.search(next_block.text) and block.role in {
        "formula_placeholder",
        "shape_placeholder",
        "image_placeholder",
    }:
        return _StartDecision(True, 0.58, "placeholder_before_question", True, None)

    return _StartDecision(False, 0.35, "continuation", True, None)


def detect_problem_end(current_group: _GroupState, next_block: _Line | None) -> tuple[bool, str]:
    """Decide whether the current group should end before next_block."""
    if not current_group.lines or next_block is None:
        return False, ""

    last = current_group.last_line
    assert last is not None
    gap = next_block.y0 - last.y1

    if gap > HARD_SPLIT_GAP:
        return True, "large_vertical_gap"

    bbox_h = max(0.0, _group_bbox(current_group.lines).y1 - _group_bbox(current_group.lines).y0)
    if bbox_h > 350 and _is_question_like_text(next_block.text):
        return True, "oversized_group_before_new_question"

    if _is_secondary_problem_start(next_block, last):
        return True, "new_question_cue_detected"

    if last.role in {"formula_placeholder", "shape_placeholder", "image_placeholder"} and _is_question_like_text(next_block.text):
        return True, "placeholder_then_new_question"

    if _is_composite_tail(current_group.lines) and _is_secondary_problem_start(next_block, last):
        return True, "composite_finished_then_new_problem"

    return False, ""


def should_split_before(block: _Line, current_group: _GroupState) -> bool:
    """Return True when block should start a new group."""
    if not current_group.lines:
        return False
    last = current_group.last_line
    assert last is not None

    if block.role in {"header_meta", "score_meta"}:
        return False

    if _is_secondary_problem_start(block, last):
        return True

    if (block.y0 - last.y1) > HARD_SPLIT_GAP and _is_question_like_text(block.text):
        return True

    if _group_height(current_group.lines) > 330 and _is_question_like_text(block.text):
        return True

    return False


def should_attach_block(block: _Line, current_group: _GroupState) -> bool:
    """Return True when block should be appended to current group."""
    if not current_group.lines:
        return True

    last = current_group.last_line
    assert last is not None
    gap = block.y0 - last.y1

    if block.role in {"header_meta", "score_meta"}:
        return False

    if block.role in {"choice_marker", "subitem_marker"}:
        return True

    if gap <= MAX_ATTACH_GAP:
        return True

    if block.role in {"formula_placeholder", "shape_placeholder", "image_placeholder"} and gap <= (MAX_ATTACH_GAP + 12):
        return True

    if _is_question_like_text(block.text) and _group_has_question_text(current_group.lines):
        return False

    return gap <= (MAX_ATTACH_GAP + 8)


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
    role = _classify_line_role(text)
    return _Line(
        text=text,
        block_ids=[b.block_id for b in ordered],
        x0=min(b.bbox.x0 for b in ordered),
        y0=min(b.bbox.y0 for b in ordered),
        x1=max(b.bbox.x1 for b in ordered),
        y1=max(b.bbox.y1 for b in ordered),
        role=role,
    )


def _is_header_footer_line(line: _Line, page: SourcePage) -> bool:
    text = line.text.strip()
    if not text:
        return True

    top_ratio = line.y0 / max(page.height, 1.0)
    bottom_ratio = line.y1 / max(page.height, 1.0)

    if top_ratio < HEADER_TOP_RATIO and (HEADER_FOOTER_HINT.search(text) or META_HINT.search(text)):
        return True
    if bottom_ratio > FOOTER_BOTTOM_RATIO and (PAGE_NUMBER_ONLY.match(text) or HEADER_FOOTER_HINT.search(text)):
        return True
    return False


def _group_lines_into_candidates(lines: list[_Line], page: SourcePage) -> list[_GroupState]:
    groups: list[_GroupState] = []
    current = _GroupState()

    for idx, line in enumerate(lines):
        prev = lines[idx - 1] if idx > 0 else None
        nxt = lines[idx + 1] if idx + 1 < len(lines) else None

        if not current.lines:
            start = detect_problem_start(line, prev, nxt)
            if not start.is_start and line.role in {"header_meta", "score_meta"}:
                continue
            current = _GroupState(
                lines=[line],
                notes=[],
                start_reason=start.reason,
                start_score=start.score,
                is_probable_problem=start.is_probable_problem,
                problem_number=start.problem_number,
            )
            if line.role in {"formula_placeholder", "shape_placeholder", "image_placeholder"}:
                current.notes.append(W_PLACEHOLDER_MIXED)
            continue

        close_now, end_reason = detect_problem_end(current, line)
        if close_now or should_split_before(line, current):
            if end_reason:
                current.notes.append(end_reason)
            groups.append(current)
            start = detect_problem_start(line, prev, nxt)
            current = _GroupState(
                lines=[line],
                notes=[],
                start_reason=start.reason,
                start_score=start.score,
                is_probable_problem=start.is_probable_problem,
                problem_number=start.problem_number,
            )
            if line.role in {"formula_placeholder", "shape_placeholder", "image_placeholder"}:
                current.notes.append(W_PLACEHOLDER_MIXED)
            continue

        if should_attach_block(line, current):
            current.add_line(line)
            if line.role in {"formula_placeholder", "shape_placeholder", "image_placeholder"}:
                current.notes.append(W_PLACEHOLDER_MIXED)
        else:
            current.notes.append(W_TRUNCATED_SUSPECTED)
            groups.append(current)
            start = detect_problem_start(line, prev, nxt)
            current = _GroupState(
                lines=[line],
                notes=[W_TRUNCATED_SUSPECTED],
                start_reason=start.reason,
                start_score=start.score,
                is_probable_problem=True,
                problem_number=start.problem_number,
            )

    if current.lines:
        groups.append(current)

    if not groups and lines:
        groups.append(
            _GroupState(
                lines=list(lines),
                notes=[W_HARD_REJECT],
                start_reason="meta_only_fallback",
                start_score=0.10,
                is_probable_problem=False,
                problem_number=None,
            )
        )

    return groups


def _split_merged_groups_second_pass(groups: list[_GroupState], page: SourcePage) -> list[_GroupState]:
    out: list[_GroupState] = []
    for group in groups:
        lines = group.lines
        if len(lines) < 2:
            out.append(group)
            continue

        group_text = " ".join(ln.text for ln in lines)
        question_count = len(QUESTION_ENDING.findall(group_text))
        too_tall = _group_height(lines) > page.height * MERGED_REGION_RATIO
        too_many_blocks = sum(len(ln.block_ids) for ln in lines) >= MERGED_BLOCK_COUNT
        mid_starts = _secondary_start_indices(lines)

        if (question_count >= 2 or too_tall or too_many_blocks) and mid_starts:
            split_points = sorted(set([0, *mid_starts]))
            for i, s in enumerate(split_points):
                e = split_points[i + 1] if i + 1 < len(split_points) else len(lines)
                seg = lines[s:e]
                if not seg:
                    continue
                new_group = _GroupState(
                    lines=seg,
                    notes=list(group.notes) + [W_MERGED_SUSPECTED],
                    start_reason=f"{group.start_reason}+second_pass_split",
                    start_score=min(0.90, group.start_score + 0.04),
                    is_probable_problem=True,
                    problem_number=group.problem_number if i == 0 else _extract_problem_number(seg[0].text),
                )
                out.append(new_group)
            continue

        if question_count >= 2 and not mid_starts:
            group.notes.append(W_MERGED_SUSPECTED)

        out.append(group)
    return out


def _group_to_region(group: _GroupState, page: SourcePage, idx: int) -> RawProblemRegion:
    bbox = _group_bbox(group.lines)
    block_ids = [bid for ln in group.lines for bid in ln.block_ids]
    notes = sorted(set(group.notes))

    if _is_composite_tail(group.lines):
        notes.append(W_COMPOSITE)

    subitems = _extract_subitems_from_lines(group.lines)

    confidence = _compute_confidence(group, notes)
    probable = group.is_probable_problem and confidence >= 0.30

    return RawProblemRegion(
        region_id=f"{page.page_id}_r{idx:04d}",
        document_id=page.document_id,
        source_path=page.source_path,
        page_number=page.page_number,
        problem_number=group.problem_number,
        bbox=bbox,
        text_block_ids=block_ids,
        visual_block_ids=[],
        notes=notes,
        segmentation_score=confidence,
        segmentation_reason=group.start_reason,
        is_probable_problem=probable,
        subitems=subitems,
    )


def _split_oversized_region(page: SourcePage, region: RawProblemRegion, lines: list[_Line]) -> list[RawProblemRegion]:
    in_region = [ln for ln in lines if ln.y0 >= region.bbox.y0 and ln.y1 <= region.bbox.y1]
    if len(in_region) < 2:
        return []

    split_indices = [0]
    for idx in range(1, len(in_region)):
        prev = in_region[idx - 1]
        cur = in_region[idx]
        if _is_secondary_problem_start(cur, prev):
            split_indices.append(idx)
            continue
        if (cur.y0 - prev.y1) > HARD_SPLIT_GAP:
            split_indices.append(idx)

    split_indices = sorted(set(split_indices))
    if len(split_indices) <= 1:
        return []

    splits: list[RawProblemRegion] = []
    for i, s in enumerate(split_indices, start=1):
        e = split_indices[i] if i < len(split_indices) else len(in_region)
        seg_lines = in_region[s:e]
        if not seg_lines:
            continue
        bbox = BBox(
            x0=min(ln.x0 for ln in seg_lines),
            y0=min(ln.y0 for ln in seg_lines),
            x1=max(ln.x1 for ln in seg_lines),
            y1=max(ln.y1 for ln in seg_lines),
        )
        split_group = _GroupState(lines=seg_lines, notes=[W_OVERSIZED_RETRY], start_reason=f"{region.segmentation_reason}+oversized_split_retry", start_score=min(0.88, region.segmentation_score + 0.04), is_probable_problem=True)
        splits.append(
            RawProblemRegion(
                region_id=f"{region.region_id}_s{i:02d}",
                document_id=page.document_id,
                source_path=page.source_path,
                page_number=page.page_number,
                problem_number=_extract_problem_number(seg_lines[0].text),
                bbox=bbox,
                text_block_ids=[bid for ln in seg_lines for bid in ln.block_ids],
                visual_block_ids=[],
                notes=[W_OVERSIZED_RETRY],
                segmentation_score=_compute_confidence(split_group, [W_OVERSIZED_RETRY]),
                segmentation_reason=f"{region.segmentation_reason}+oversized_split_retry",
                is_probable_problem=True,
                subitems=_extract_subitems_from_lines(seg_lines),
            )
        )
    return splits


def _compute_confidence(group: _GroupState, notes: list[str]) -> float:
    text = " ".join(ln.text for ln in group.lines)
    score = group.start_score

    if QUESTION_ENDING.search(text):
        score += 0.15
    if QUESTION_BODY.search(text):
        score += 0.10
    if CHOICE_MARKER.search(text) or _is_composite_tail(group.lines):
        score += 0.08
    if re.search(r"\d", text):
        score += 0.05

    placeholder_count = sum(1 for ln in group.lines if "placeholder" in ln.role)
    meta_count = sum(1 for ln in group.lines if ln.role in {"header_meta", "score_meta"})

    if placeholder_count and not QUESTION_BODY.search(text):
        score -= 0.14
    if meta_count > 0:
        score -= 0.16
    if W_MERGED_SUSPECTED in notes:
        score -= 0.10
    if W_TRUNCATED_SUSPECTED in notes:
        score -= 0.08
    if len(text) < 8:
        score -= 0.12

    return max(0.0, min(1.0, score))


def _classify_line_role(text: str) -> str:
    s = text.strip()
    if not s:
        return "empty"
    if PLACEHOLDER_FORMULA.search(s):
        return "formula_placeholder"
    if PLACEHOLDER_SHAPE.search(s):
        return "shape_placeholder"
    if PLACEHOLDER_IMAGE.search(s) or PLACEHOLDER_GENERIC.search(s):
        return "image_placeholder"
    if CHOICE_MARKER.search(s):
        return "choice_marker"
    if SUBITEM_MARKER.search(s):
        return "subitem_marker"
    if META_HINT.search(s):
        return "score_meta"
    if HEADER_FOOTER_HINT.search(s) and not QUESTION_BODY.search(s):
        return "header_meta"
    return "text"


def _extract_problem_number(text: str) -> str | None:
    m = PROBLEM_NUMBER.match(text.strip())
    return m.group(1) if m else None


def _is_secondary_problem_start(block: _Line, prev: _Line | None) -> bool:
    if block.role in {"subitem_marker", "choice_marker", "header_meta", "score_meta"}:
        return False
    if EXPLICIT_PROBLEM_MARKER.match(block.text):
        return True
    if _is_question_like_text(block.text):
        if prev is None:
            return True
        return (block.y0 - prev.y1) > 12
    return False


def _secondary_start_indices(lines: list[_Line]) -> list[int]:
    idxs: list[int] = []
    for i in range(1, len(lines)):
        if _is_secondary_problem_start(lines[i], lines[i - 1]):
            idxs.append(i)
    return idxs


def _extract_subitems_from_lines(lines: list[_Line]) -> list[RawSubItem]:
    subitems: list[RawSubItem] = []
    current_label: str | None = None
    current_lines: list[_Line] = []

    for line in lines:
        label = _extract_subitem_label(line.text)
        if label:
            if current_label and current_lines:
                subitems.append(_build_raw_subitem(current_label, current_lines))
            current_label = label
            current_lines = [line]
        elif current_label is not None:
            current_lines.append(line)

    if current_label and current_lines:
        subitems.append(_build_raw_subitem(current_label, current_lines))

    return subitems


def _extract_subitems_from_ids(
    block_ids: list[str],
    text_by_id: dict[str, str],
    block_by_id: dict[str, object],
) -> list[ProblemSubItem]:
    subitems: list[ProblemSubItem] = []
    current_label: str | None = None
    current_ids: list[str] = []

    for bid in block_ids:
        text = (text_by_id.get(bid) or "").strip()
        label = _extract_subitem_label(text)
        if label:
            if current_label and current_ids:
                subitems.append(_build_problem_subitem(current_label, current_ids, text_by_id, block_by_id))
            current_label = label
            current_ids = [bid]
        elif current_label is not None:
            current_ids.append(bid)

    if current_label and current_ids:
        subitems.append(_build_problem_subitem(current_label, current_ids, text_by_id, block_by_id))
    return subitems


def _build_raw_subitem(label: str, lines: list[_Line]) -> RawSubItem:
    text = " ".join(ln.text for ln in lines).strip()
    bbox = BBox(
        x0=min(ln.x0 for ln in lines),
        y0=min(ln.y0 for ln in lines),
        x1=max(ln.x1 for ln in lines),
        y1=max(ln.y1 for ln in lines),
    )
    return RawSubItem(
        label=label,
        text=text,
        source_block_ids=[bid for ln in lines for bid in ln.block_ids],
        bbox=bbox,
    )


def _build_problem_subitem(
    label: str,
    ids: list[str],
    text_by_id: dict[str, str],
    block_by_id: dict[str, object],
) -> ProblemSubItem:
    text = " ".join((text_by_id.get(i) or "").strip() for i in ids).strip()
    bboxes = [block_by_id[i].bbox for i in ids if i in block_by_id]
    bbox = None
    if bboxes:
        bbox = BBox(
            x0=min(b.x0 for b in bboxes),
            y0=min(b.y0 for b in bboxes),
            x1=max(b.x1 for b in bboxes),
            y1=max(b.y1 for b in bboxes),
        )
    return ProblemSubItem(label=label, text=text, source_block_ids=ids, bbox=bbox)


def _extract_subitem_label(text: str) -> str | None:
    m = SUBITEM_MARKER.match(text.strip())
    if not m:
        return None
    return m.group(0)


def _is_composite_tail(lines: list[_Line]) -> bool:
    text = " ".join(ln.text for ln in lines)
    has_directive = "다음을" in text and ("계산" in text or "물음" in text)
    has_subitems = len(_extract_subitems_from_lines(lines)) >= 2
    return has_directive and has_subitems


def _group_bbox(lines: list[_Line]) -> BBox:
    return BBox(
        x0=min(ln.x0 for ln in lines),
        y0=min(ln.y0 for ln in lines),
        x1=max(ln.x1 for ln in lines),
        y1=max(ln.y1 for ln in lines),
    )


def _group_height(lines: list[_Line]) -> float:
    bbox = _group_bbox(lines)
    return max(0.0, bbox.y1 - bbox.y0)


def _group_has_question_text(lines: list[_Line]) -> bool:
    return _is_question_like_text(" ".join(ln.text for ln in lines))


def _is_oversized(region: RawProblemRegion, page: SourcePage) -> bool:
    h = max(0.0, region.bbox.y1 - region.bbox.y0)
    return h >= page.height * OVERSIZED_REGION_RATIO


def _is_hard_reject_candidate(cand: ProblemCandidate) -> bool:
    text = cand.text.strip()
    if len(text) < 4:
        return True
    if PAGE_NUMBER_ONLY.match(text):
        return True
    if _is_top_meta_without_number(cand):
        return True
    if _looks_like_header_metadata_pattern(text):
        return True
    if HEADER_FOOTER_HINT.search(text) and not _is_question_like_text(text):
        return True
    if META_HINT.search(text) and not _is_question_like_text(text):
        return True
    return not cand.is_probable_problem and not _is_question_like_text(text)


def _is_top_meta_without_number(cand: ProblemCandidate) -> bool:
    return (
        cand.problem_number is None
        and cand.page_height is not None
        and cand.bbox.y0 < cand.page_height * 0.28
    )


def _looks_like_header_metadata_pattern(text: str) -> bool:
    if len(text) > 120:
        return False
    if text.count(":") >= 2:
        return True
    return bool(COLON_META.search(text) and META_HINT.search(text))


def _is_question_like_text(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    return bool(QUESTION_ENDING.search(t) or QUESTION_BODY.search(t) or QUESTION_START.search(t))


def _has_merged_signal(cand: ProblemCandidate) -> bool:
    text = cand.text
    question_count = len(QUESTION_ENDING.findall(text))
    too_many_blocks = len(cand.source_block_ids) >= MERGED_BLOCK_COUNT
    too_tall = bool(cand.page_height and (cand.bbox.y1 - cand.bbox.y0) > cand.page_height * MERGED_REGION_RATIO)
    return question_count >= 2 or too_many_blocks or too_tall


def _has_truncated_signal(cand: ProblemCandidate) -> bool:
    t = cand.text.strip()
    if len(t) < 10:
        return True
    if t.endswith("..."):
        return True
    return False




