from modu_semantic.rag.retrieve import retrieve_examples_from_entries, score_entry


def _entry(problem_id: str, **kwargs):
    base = {
        "problem_id": problem_id,
        "py_path": f"{problem_id}/{problem_id}.py",
        "semantic_path": f"{problem_id}/output/json/{problem_id}.semantic.json",
        "layout_path": f"{problem_id}/output/json/{problem_id}.layout.json",
        "tags": [],
        "validation_passed": True,
        "updated_at": "2026-01-01T00:00:00+00:00",
        "problem_type": "unknown",
        "grade": "unknown",
        "topic": "unknown",
        "visual_primitives": [],
        "layout_pattern": "unknown",
        "answer_style": "unknown",
        "failure_notes": "",
        "source_image_hash": "",
    }
    base.update(kwargs)
    return base


def test_retrieve_score_prefers_matching_problem_type_and_tags() -> None:
    input_meta = {
        "problem_type": "geometry",
        "tags": ["triangle", "area"],
        "visual_primitives": ["polygon", "text"],
        "layout_pattern": "medium",
    }

    e1 = _entry(
        "e1",
        problem_type="geometry",
        tags=["triangle", "area"],
        visual_primitives=["polygon", "text"],
        layout_pattern="medium",
        validation_passed=True,
    )
    e2 = _entry(
        "e2",
        problem_type="arithmetic",
        tags=["addition"],
        visual_primitives=["text"],
        layout_pattern="simple",
        validation_passed=True,
    )

    assert score_entry(input_meta, e1) > score_entry(input_meta, e2)


def test_retrieve_top_k_returns_sorted_examples() -> None:
    input_meta = {"problem_type": "geometry", "tags": ["triangle"]}

    entries = [
        _entry("a", problem_type="geometry", tags=["triangle"], validation_passed=True),
        _entry("b", problem_type="geometry", tags=[], validation_passed=False),
        _entry("c", problem_type="unknown", tags=["triangle"], validation_passed=True),
    ]

    top = retrieve_examples_from_entries(input_meta, entries, top_k=2)
    assert len(top) == 2
    assert top[0]["entry"]["problem_id"] == "a"
    assert top[1]["entry"]["problem_id"] in {"b", "c"}
    assert top[0]["score"] >= top[1]["score"]
