from pathlib import Path

from math_problem_pipeline.extract.problem_segmenter import regions_to_candidates, segment_page_to_regions
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
        source_path="doc.pdf",
        page_number=1,
        width=595.0,
        height=842.0,
        text_blocks=blocks,
        visual_blocks=[],
    )


def test_header_and_school_mark_not_segmented_as_problem() -> None:
    page = _page(
        [
            _block("b1", "단원평가", 40, 30, 120, 45),
            _block("b2", "OO초등학교", 150, 30, 260, 45),
            _block("b3", "1.", 40, 120, 50, 135),
            _block("b4", "다음 중 옳은 것은?", 60, 120, 200, 135),
            _block("b5", "① 2", 70, 145, 120, 160),
            _block("b6", "② 3", 140, 145, 190, 160),
        ]
    )

    regions = segment_page_to_regions(page)
    candidates = regions_to_candidates(regions, page)
    assert len(candidates) >= 1
    assert all("단원평가" not in c.text for c in candidates)


def test_multiple_questions_not_merged_into_one_candidate() -> None:
    page = _page(
        [
            _block("b1", "1.", 40, 120, 50, 135),
            _block("b2", "3 + 5 = ?", 60, 120, 130, 135),
            _block("b3", "2.", 40, 200, 50, 215),
            _block("b4", "7 - 4 = ?", 60, 200, 130, 215),
        ]
    )

    regions = segment_page_to_regions(page)
    candidates = regions_to_candidates(regions, page)
    assert len(candidates) >= 2


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


