import json
from pathlib import Path

from modu_semantic.rag.meta_recommender import recommend_input_meta, tune_meta_from_ocr_features


def _write_index(index_path: Path) -> None:
    row = {
        "problem_id": "0017",
        "py_path": "0017/0017.py",
        "semantic_path": "0017/output/json/0017.semantic.json",
        "tags": ["word_problem", "multiplication"],
        "validation_passed": True,
        "updated_at": "2026-01-01T00:00:00+00:00",
        "problem_type": "arithmetic_word_problem",
        "grade": "unknown",
        "topic": "unknown",
        "visual_primitives": ["text", "rect"],
        "layout_pattern": "medium",
        "answer_style": "blank",
        "failure_notes": "",
        "source_image_hash": "",
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")


def test_recommend_input_meta_from_image_filename_and_index(tmp_path: Path) -> None:
    index_path = tmp_path / "index.jsonl"
    _write_index(index_path)

    meta = recommend_input_meta(
        explicit_meta=None,
        index_path=index_path,
        image_path=tmp_path / "0017.png",
    )

    assert meta["problem_id"] == "0017"
    assert meta["problem_type"] == "arithmetic_word_problem"
    assert "word_problem" in meta["tags"]
    assert meta["layout_pattern"] == "medium"
    assert meta["visual_primitives"] == ["text", "rect"]


def test_recommend_input_meta_keeps_explicit_fields(tmp_path: Path) -> None:
    index_path = tmp_path / "index.jsonl"
    _write_index(index_path)

    meta = recommend_input_meta(
        explicit_meta={"problem_id": "0017", "problem_type": "custom_type", "tags": ["manual"]},
        index_path=index_path,
        image_path=tmp_path / "0017.png",
    )

    assert meta["problem_id"] == "0017"
    assert meta["problem_type"] == "custom_type"
    assert "manual" in meta["tags"]


def test_tune_meta_from_ocr_features_infers_problem_type_and_tags() -> None:
    tuned = tune_meta_from_ocr_features(
        {
            "problem_type": "unknown",
            "tags": ["0017", "ol", "nu"],
            "layout_pattern": "unknown",
            "ocr_text_lines": ["17x▲=■", "64÷▲=8", "얼마를 나타냅니까?"],
            "ocr_boxes": [{"text": "17x", "x": 0, "y": 0, "width": 10, "height": 10, "confidence": 80.0}],
            "visual_primitives": [],
        }
    )

    assert tuned["problem_type"] == "arithmetic_equation"
    assert "equation" in tuned["tags"]
    assert "arithmetic" in tuned["tags"]
    assert "ol" not in tuned["tags"]
    assert tuned["layout_pattern"] == "medium"
