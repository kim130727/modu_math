from pathlib import Path

from math_problem_pipeline.extract.problem_segmenter import (
    filter_obvious_non_problems,
    regions_to_candidates,
    segment_page_to_regions,
)
from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.raw_models import BBox, RawTextBlock, SourcePage
from math_problem_pipeline.models.semantic_models import FractionPartition, FractionShadedAreaProblem
from math_problem_pipeline.normalize.semantic_builder import candidate_to_extracted, extracted_to_semantic
from math_problem_pipeline.normalize.type_classifier import classify_problem_type
from math_problem_pipeline.render.svg_renderer import render_problem_to_svg


def _block(block_id: str, text: str, x0: float, y0: float, x1: float, y1: float) -> RawTextBlock:
    return RawTextBlock(block_id=block_id, text=text, bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1))


def _page(blocks: list[RawTextBlock]) -> SourcePage:
    return SourcePage(
        page_id="doc_p0001",
        document_id="doc",
        source_path="doc.hwpx",
        page_number=1,
        width=595.0,
        height=842.0,
        text_blocks=blocks,
        visual_blocks=[],
    )


def _candidate_texts(page: SourcePage) -> list[str]:
    regions = segment_page_to_regions(page)
    candidates = regions_to_candidates(regions, page)
    return [c.text for c in candidates]


def test_header_meta_is_rejected() -> None:
    page = _page(
        [
            _block("b1", "Date: 2026-04-01", 40, 25, 180, 40),
            _block("b2", "Name: Student", 200, 25, 320, 40),
            _block("b3", "Score: 100", 360, 25, 470, 40),
        ]
    )
    candidates = regions_to_candidates(segment_page_to_regions(page), page)
    accepted, rejected = filter_obvious_non_problems(candidates)

    assert len(accepted) == 0
    assert len(rejected) >= 1
    assert any("rejected_non_problem_candidate" in c.warnings for c in rejected)


def test_eraser_question_and_card_question_are_split() -> None:
    page = _page(
        [
            _block("b1", "1.", 40, 120, 50, 135),
            _block("b2", "지우개의 길이는 몇 mm입니까?", 60, 120, 260, 138),
            _block("b3", "수식입니다.", 64, 145, 130, 160),
            _block("b4", "3장의 수 카드를 모두 한 번씩만 사용하여", 60, 200, 300, 218),
            _block("b5", "알맞은 수를 구하시오.", 60, 223, 220, 241),
        ]
    )

    texts = _candidate_texts(page)
    assert len(texts) >= 2
    assert any("지우개의 길이는" in t for t in texts)
    assert any("3장의 수 카드를" in t for t in texts)


def test_division_question_and_movie_time_question_are_split() -> None:
    page = _page(
        [
            _block("b1", "큰 수를 작은 수로 나눈 몫을 구하시오.", 52, 120, 300, 140),
            _block("b2", "그림입니다.", 56, 145, 130, 160),
            _block("b3", "영화가 오전 8시 30분에 시작합니다.", 52, 210, 300, 230),
            _block("b4", "몇 시 몇 분에 끝납니까?", 52, 234, 220, 252),
        ]
    )

    texts = _candidate_texts(page)
    assert len(texts) >= 2
    assert any("큰 수를 작은 수로 나눈" in t for t in texts)
    assert any("영화가 오전" in t for t in texts)


def test_clock_question_not_rejected() -> None:
    page = _page(
        [
            _block("b1", "시계를 보고 몇 시 몇 분인지 쓰시오.", 50, 160, 280, 180),
            _block("b2", "그림입니다.", 60, 186, 120, 200),
        ]
    )

    candidates = regions_to_candidates(segment_page_to_regions(page), page)
    accepted, rejected = filter_obvious_non_problems(candidates)

    assert len(accepted) >= 1
    assert all("rejected_non_problem_candidate" not in c.warnings for c in accepted)
    assert not any("시계를 보고" in c.text for c in rejected)


def test_composite_problem_detected() -> None:
    page = _page(
        [
            _block("b1", "다음을 계산하시오.", 50, 140, 200, 158),
            _block("b2", "(1) 12 + 8", 58, 170, 160, 188),
            _block("b3", "(2) 30 - 7", 58, 196, 160, 214),
            _block("b4", "(3) 5 x 6", 58, 222, 160, 240),
        ]
    )

    candidates = regions_to_candidates(segment_page_to_regions(page), page)
    assert len(candidates) >= 1
    assert any("composite_problem_detected" in c.warnings for c in candidates)
    assert any(len(c.subitems) >= 2 for c in candidates)


def test_choice_with_formula_placeholder_kept() -> None:
    page = _page(
        [
            _block("b1", "1.", 40, 120, 50, 135),
            _block("b2", "옳은 것을 고르시오.", 60, 120, 180, 138),
            _block("b3", "① 수식입니다.", 68, 150, 180, 168),
            _block("b4", "② 24", 68, 176, 120, 194),
        ]
    )

    candidates = regions_to_candidates(segment_page_to_regions(page), page)
    assert len(candidates) >= 1
    text = " ".join(c.text for c in candidates)
    assert "① 수식입니다." in text
    assert any("placeholder_mixed_with_text" in c.warnings for c in candidates)


def test_placeholder_not_overmerged_with_next_question() -> None:
    page = _page(
        [
            _block("b1", "2.", 40, 120, 50, 135),
            _block("b2", "길이를 재어 보시오.", 60, 120, 170, 138),
            _block("b3", "모서리가 둥근사각형입니다.", 60, 146, 240, 164),
            _block("b4", "3.", 40, 220, 50, 235),
            _block("b5", "3장의 수 카드를 사용하여 수를 만드시오.", 60, 220, 280, 238),
        ]
    )

    texts = _candidate_texts(page)
    assert len(texts) >= 2
    assert any("길이를 재어" in t for t in texts)
    assert any("3장의 수 카드" in t for t in texts)


def test_long_fraction_division_text_not_classified_as_fraction_shaded_area() -> None:
    candidate = ProblemCandidate(
        candidate_id="c1",
        source_path="doc.pdf",
        page_number=1,
        problem_number="1",
        bbox=BBox(x0=0, y0=100, x1=400, y1=220),
        text="77과 1122를 이용하여 분수의 나눗셈 과정을 서술하시오. 계산 과정을 자세히 적으시오.",
        source_block_ids=["b1"],
        confidence=0.9,
        warnings=[],
        is_probable_problem=True,
        segmentation_reason="explicit_problem_marker",
        page_width=595,
        page_height=842,
    )

    guess = classify_problem_type(candidate)
    assert guess.type_name != "fraction_shaded_area"


def test_abnormal_total_parts_not_generated_from_noise_numbers() -> None:
    candidate = ProblemCandidate(
        candidate_id="c2",
        source_path="doc.pdf",
        page_number=1,
        problem_number="2",
        bbox=BBox(x0=0, y0=100, x1=400, y1=220),
        text="도형을 보고 77과 1122를 비교하여 설명하시오. 부분과 전체의 의미를 쓰시오.",
        source_block_ids=["b1"],
        confidence=0.8,
        warnings=[],
        is_probable_problem=True,
        segmentation_reason="layout_gap_and_alignment_change",
        page_width=595,
        page_height=842,
    )

    semantic = extracted_to_semantic(candidate_to_extracted(candidate))
    if semantic.type == "fraction_shaded_area":
        assert semantic.fraction.total_parts <= 24


def test_svg_renderer_falls_back_for_invalid_fraction_structure(tmp_path: Path) -> None:
    semantic = FractionShadedAreaProblem(
        problem_id="bad_fraction",
        source_path="doc.pdf",
        page_number=1,
        type="fraction_shaded_area",
        question_text="색칠된 부분의 분수를 구하세요.",
        fraction=FractionPartition(shape="rectangle", total_parts=77, shaded_parts=3, rows=7, cols=8),
        warnings=[],
    )

    out_svg = tmp_path / "bad_fraction.render.svg"
    meta = render_problem_to_svg(semantic, out_svg)

    svg = out_svg.read_text(encoding="utf-8")
    assert meta["fallback_render_used"] is True
    assert "fallback render" in svg
    assert "#7db7ff" not in svg

